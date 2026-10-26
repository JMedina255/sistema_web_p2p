from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.profile import DisponibilidadHoraria, PerfilAcademico
from app.schemas.recommendation import (
    MentorRecommendationItem,
    OfferRecommendationItem,
    RecommendationExplainResponse,
    RecommendationListResponse,
    ScoreBreakdown,
)
from app.services.offer_service import OfferService
from app.services.profile_service import ProfileService, get_profile_in_memory

# Mapeo de ponderadores de asignaturas críticas de la EPIS-UPT
CRITICAL_COURSE_WEIGHTS: dict[int, float] = {
    1: 1.2,  # Cálculo I
    2: 1.2,  # Cálculo II
    3: 1.3,  # Algoritmos y Estructuras de Datos
    4: 1.2,  # Programación Orientada a Objetos
    5: 1.1,  # Base de Datos
}

COURSE_METADATA: dict[int, tuple[str, str]] = {
    1: ("CALC-101", "Cálculo I"),
    2: ("CALC-201", "Cálculo II"),
    3: ("ALGO-202", "Algoritmos y Estructuras de Datos"),
    4: ("POO-301", "Programación Orientada a Objetos"),
    5: ("BDD-401", "Base de Datos"),
}

DIA_NOMBRES: dict[int, str] = {
    1: "Lun",
    2: "Mar",
    3: "Mie",
    4: "Jue",
    5: "Vie",
    6: "Sab",
    7: "Dom",
}

# Mentores semilla para pruebas y desarrollo en memoria
_DEFAULT_SYNTHETIC_MENTORS: list[dict] = [
    {
        "email": "2022073504@upt.pe",
        "codigo_estudiante": "2022073504",
        "nombres": "Renzo Antonio",
        "apellidos": "Antayhua Mamani",
        "ciclo_actual": 7,
        "rol_postulacion": "mentor",
        "materias_interes": [1, 3],
        "temas_seleccionados": [1, 2, 9, 10],
        "modalidad_preferida": "presencial",
        "disponibilidad": [
            {"dia_semana": 1, "hora_inicio": "08:00", "hora_fin": "09:00"},
            {"dia_semana": 1, "hora_inicio": "09:00", "hora_fin": "10:00"},
            {"dia_semana": 3, "hora_inicio": "14:00", "hora_fin": "15:00"},
            {"dia_semana": 3, "hora_inicio": "15:00", "hora_fin": "16:00"},
            {"dia_semana": 5, "hora_inicio": "10:00", "hora_fin": "11:00"},
        ],
    },
    {
        "email": "mentor.avanzado@upt.pe",
        "codigo_estudiante": "2020061234",
        "nombres": "Carlos Alberto",
        "apellidos": "Mendoza Dávila",
        "ciclo_actual": 9,
        "rol_postulacion": "mentor",
        "materias_interes": [3, 4, 5],
        "temas_seleccionados": [9, 11, 14, 18, 19],
        "modalidad_preferida": "virtual",
        "disponibilidad": [
            {"dia_semana": 2, "hora_inicio": "10:00", "hora_fin": "11:00"},
            {"dia_semana": 2, "hora_inicio": "11:00", "hora_fin": "12:00"},
            {"dia_semana": 4, "hora_inicio": "15:00", "hora_fin": "16:00"},
            {"dia_semana": 4, "hora_inicio": "16:00", "hora_fin": "17:00"},
        ],
    },
    {
        "email": "mentora.redes@upt.pe",
        "codigo_estudiante": "2021069876",
        "nombres": "Elena Patricia",
        "apellidos": "Vega Morales",
        "ciclo_actual": 8,
        "rol_postulacion": "mentor",
        "materias_interes": [1, 2, 3],
        "temas_seleccionados": [1, 3, 5, 9, 12],
        "modalidad_preferida": "hibrida",
        "disponibilidad": [
            {"dia_semana": 1, "hora_inicio": "09:00", "hora_fin": "10:00"},
            {"dia_semana": 3, "hora_inicio": "15:00", "hora_fin": "16:00"},
            {"dia_semana": 5, "hora_inicio": "16:00", "hora_fin": "17:00"},
        ],
    },
    {
        "email": "mentor.x.senior@upt.pe",
        "codigo_estudiante": "2019055555",
        "nombres": "Fernando Javier",
        "apellidos": "Rojas Tapia",
        "ciclo_actual": 10,
        "rol_postulacion": "mentor",
        "materias_interes": [4, 5],
        "temas_seleccionados": [15, 16, 20, 21],
        "modalidad_preferida": "presencial",
        "disponibilidad": [
            {"dia_semana": 6, "hora_inicio": "09:00", "hora_fin": "10:00"},
            {"dia_semana": 6, "hora_inicio": "10:00", "hora_fin": "11:00"},
        ],
    },
    {
        # Mentor inelegible intencional por no cumplir RN-03 (ciclo < VII)
        "email": "estudiante.junior@upt.pe",
        "codigo_estudiante": "2023078888",
        "nombres": "Mateo",
        "apellidos": "Flores Quispe",
        "ciclo_actual": 4,
        "rol_postulacion": "mentoreado",
        "materias_interes": [1],
        "temas_seleccionados": [1],
        "modalidad_preferida": "presencial",
        "disponibilidad": [],
    },
]


def jaccard_similarity(set_a: set, set_b: set) -> float:
    """Calcula el coeficiente de similitud de Jaccard entre dos conjuntos."""
    if not set_a and not set_b:
        return 0.0
    union = set_a | set_b
    if not union:
        return 0.0
    return len(set_a & set_b) / len(union)


def dice_similarity(set_a: set, set_b: set) -> float:
    """Calcula el coeficiente de coincidencia de Dice entre dos conjuntos."""
    denom = len(set_a) + len(set_b)
    if denom == 0:
        return 0.0
    return (2.0 * len(set_a & set_b)) / denom


def compute_modality_compatibility(modality_mentee: str | None, modality_mentor: str | None) -> float:
    """Calcula la compatibilidad entre modalidades pedagógicas."""
    m_mentee = (modality_mentee or "presencial").strip().lower()
    m_mentor = (modality_mentor or "presencial").strip().lower()

    if m_mentee == m_mentor:
        return 1.0
    if m_mentee == "hibrida" or m_mentor == "hibrida":
        return 0.9
    # presencial vs virtual
    return 0.2


class RecommendationService:
    """
    Motor de Recomendación Inteligente Top-k (EdRecSys v1.0).
    Implementa ranking multifactorial explicable combinando:
    - RN-03: Mérito institucional (ciclo >= VII).
    - Afinidad curricular y ponderador de asignatura crítica (1.0x a 1.3x).
    - Solapamiento temático silábico (Jaccard / Dice).
    - Compatibilidad de agenda semanal (intersección en franjas 6x11).
    - Alineación de modalidad pedagógica.
    - Criterio de ordenamiento determinista con desempate multifactorial.
    """

    WEIGHT_TOPIC: float = 0.40
    WEIGHT_SCHEDULE: float = 0.35
    WEIGHT_MODALITY: float = 0.15
    WEIGHT_CURRICULAR: float = 0.10

    @classmethod
    def compute_candidate_score(
        cls,
        mentee_courses: set[int] | None,
        mentee_topics: set[int] | None,
        mentee_slots: set[tuple[int, str, str]] | None,
        mentee_modality: str | None,
        candidate_courses: set[int] | None,
        candidate_topics: set[int] | None,
        candidate_slots: set[tuple[int, str, str]] | None,
        candidate_modality: str | None,
        candidate_cycle: int,
        offer_time: datetime | None = None,
        offer_duration_minutes: int = 60,
    ) -> tuple[float, ScoreBreakdown]:
        """
        Calcula el puntaje multifactorial y genera el desglose explicable.
        """
        # Normalización defensiva contra valores None
        m_courses = set(mentee_courses) if mentee_courses is not None else set()
        m_topics = set(mentee_topics) if mentee_topics is not None else set()
        m_slots = set(mentee_slots) if mentee_slots is not None else set()
        m_modality = mentee_modality or "presencial"

        c_courses = set(candidate_courses) if candidate_courses is not None else set()
        c_topics = set(candidate_topics) if candidate_topics is not None else set()
        c_slots = set(candidate_slots) if candidate_slots is not None else set()
        c_modality = candidate_modality or "presencial"

        # 1. Validación de mérito institucional RN-03
        is_eligible = candidate_cycle >= 7
        if not is_eligible:
            breakdown = ScoreBreakdown(
                curricular_affinity=0.0,
                course_weight_factor=1.0,
                critical_course_applied=None,
                topic_overlap_jaccard=0.0,
                topic_overlap_dice=0.0,
                schedule_compatibility=0.0,
                schedule_matching_slots_count=0,
                matching_slots=[],
                modality_compatibility=0.0,
                institutional_merit_eligible=False,
                explanation_text=f"Candidato no elegible: Ciclo actual ({candidate_cycle}) inferior al requisito normativo institucional (ciclo >= VII según RN-03).",
            )
            return 0.0, breakdown

        # 2. Afinidad Curricular y Factor Ponderador Crítico
        common_courses = m_courses & c_courses
        if m_courses:
            curricular_affinity = len(common_courses) / len(m_courses)
        else:
            curricular_affinity = 1.0 if common_courses else 0.0

        # Ponderador de asignatura crítica / filtro
        course_weight = 1.0
        applied_course_code = None
        for c in common_courses:
            w = CRITICAL_COURSE_WEIGHTS.get(c, 1.0)
            if w > course_weight:
                course_weight = w
                applied_course_code = COURSE_METADATA.get(c, (f"CURSO-{c}", ""))[0]

        # 3. Solapamiento de Temas Silábicos
        jaccard = jaccard_similarity(m_topics, c_topics)
        dice = dice_similarity(m_topics, c_topics)

        # 4. Compatibilidad de Agenda Horaria Semanal
        matching_slots_readable: list[str] = []
        if offer_time is not None:
            # Para una oferta con fecha específica y duración (60 o 90 min)
            dia_oferta = offer_time.weekday() + 1
            h_start = offer_time.hour
            required_slots: list[tuple[int, str, str]] = [
                (dia_oferta, f"{h_start:02d}:00", f"{(h_start + 1) % 24:02d}:00")
            ]
            if offer_duration_minutes > 60:
                required_slots.append(
                    (dia_oferta, f"{(h_start + 1) % 24:02d}:00", f"{(h_start + 2) % 24:02d}:00")
                )

            if not m_slots:
                # Si el estudiante mentoreado no tiene agenda fijada: compatibilidad neutral 0.50 y 0 coincidencias
                schedule_score = 0.5
                matching_slots_count = 0
            else:
                matched_slots = [s for s in required_slots if s in m_slots]
                matching_slots_count = len(matched_slots)
                schedule_score = matching_slots_count / len(required_slots)
                for d, hi, hf in matched_slots:
                    dia_str = DIA_NOMBRES.get(d, f"Día {d}")
                    matching_slots_readable.append(f"{dia_str} {hi}-{hf}")
        else:
            # Para ranking de mentores: intersección de disponibilidad semanal
            common_slots = m_slots & c_slots
            matching_slots_count = len(common_slots)
            if m_slots:
                schedule_score = min(1.0, len(common_slots) / max(1, len(m_slots)))
            else:
                # Si el estudiante mentoreado no fijó horarios, asigna compatibilidad neutral
                schedule_score = 0.5

            for d, hi, hf in sorted(common_slots):
                dia_str = DIA_NOMBRES.get(d, f"Día {d}")
                matching_slots_readable.append(f"{dia_str} {hi}-{hf}")

        # 5. Compatibilidad de Modalidad
        modality_score = compute_modality_compatibility(m_modality, c_modality)

        # 6. Puntaje Multifactorial Compuesto
        score_base = (
            cls.WEIGHT_TOPIC * jaccard
            + cls.WEIGHT_SCHEDULE * schedule_score
            + cls.WEIGHT_MODALITY * modality_score
            + cls.WEIGHT_CURRICULAR * curricular_affinity
        )
        total_score = round(score_base * course_weight, 4)

        # 7. Generación de Explicabilidad Cualitativa
        explanation_parts = [
            f"Mentor ciclo {candidate_cycle} (RN-03 aprobado).",
        ]
        if applied_course_code:
            explanation_parts.append(
                f"Ponderador crítico aplicado: {course_weight:.1f}x por {applied_course_code}."
            )
        explanation_parts.append(
            f"Coincidencia temática silábica: Jaccard {jaccard * 100:.1f}%, Dice {dice * 100:.1f}%."
        )
        if not m_slots:
            explanation_parts.append(
                "El mentoreado no fijó agenda horaria previa (compatibilidad neutral 50%)."
            )
        elif matching_slots_readable:
            explanation_parts.append(
                f"Coincidencia en {matching_slots_count} franja(s) horaria(s) común(es): {', '.join(matching_slots_readable[:3])}."
            )
        else:
            explanation_parts.append("Sin coincidencia de franja horaria directa en la semana.")
        explanation_parts.append(
            f"Alineación de modalidad: {modality_score * 100:.0f}% ({m_modality} vs {c_modality})."
        )

        explanation_text = " ".join(explanation_parts)

        breakdown = ScoreBreakdown(
            curricular_affinity=round(curricular_affinity, 4),
            course_weight_factor=course_weight,
            critical_course_applied=applied_course_code,
            topic_overlap_jaccard=round(jaccard, 4),
            topic_overlap_dice=round(dice, 4),
            schedule_compatibility=round(schedule_score, 4),
            schedule_matching_slots_count=matching_slots_count,
            matching_slots=matching_slots_readable,
            modality_compatibility=round(modality_score, 4),
            institutional_merit_eligible=True,
            explanation_text=explanation_text,
        )

        return total_score, breakdown

    @classmethod
    def _get_mentee_profile_data(
        cls, db: Session | None, mentee_email: str
    ) -> tuple[set[int], set[int], set[tuple[int, str, str]], str]:
        """
        Recupera el perfil, asignaturas, temas y disponibilidad de un mentoreado.
        """
        clean_email = mentee_email.strip().lower()
        profile = ProfileService.get_profile(db, clean_email)
        avail = ProfileService.get_availability(db, clean_email)

        courses = set(profile.materias_interes) if profile.materias_interes is not None else set()
        topics = set(profile.temas_seleccionados) if profile.temas_seleccionados is not None else set()
        modality = profile.modalidad_preferida or "presencial"
        slots = set()
        for item in avail or []:
            slots.add((item.dia_semana, item.hora_inicio, item.hora_fin))

        return courses, topics, slots, modality

    @classmethod
    def get_candidate_mentors(cls, db: Session | None) -> list[dict]:
        """
        Obtiene la lista de mentores disponibles desde la base de datos o almacén semilla.
        """
        if db is not None:
            try:
                # Consultar perfiles con ciclo >= 7 o rol mentor
                rows = (
                    db.query(PerfilAcademico)
                    .filter(
                        (PerfilAcademico.ciclo_actual >= 7)
                        | (PerfilAcademico.rol_postulacion.in_(["mentor", "administrador"]))
                    )
                    .all()
                )
                mentors: list[dict] = []
                for p in rows:
                    slots_rows = (
                        db.query(DisponibilidadHoraria).filter(DisponibilidadHoraria.email == p.email).all()
                    )
                    slots_list = [
                        {
                            "dia_semana": s.dia_semana,
                            "hora_inicio": s.hora_inicio,
                            "hora_fin": s.hora_fin,
                        }
                        for s in slots_rows
                    ]
                    mentors.append(
                        {
                            "email": p.email,
                            "codigo_estudiante": p.codigo_estudiante or p.email.split("@")[0],
                            "nombres": p.nombres or "Mentor",
                            "apellidos": p.apellidos or "EPIS",
                            "ciclo_actual": p.ciclo_actual,
                            "rol_postulacion": p.rol_postulacion,
                            "materias_interes": p.materias_interes or [],
                            "temas_seleccionados": p.temas_seleccionados or [],
                            "modalidad_preferida": p.modalidad_preferida or "presencial",
                            "disponibilidad": slots_list,
                        }
                    )
                return mentors
            except Exception:
                pass

        # Fallback a mentores sintéticos si db is None o si falló la consulta en db
        return [dict(m) for m in _DEFAULT_SYNTHETIC_MENTORS]

    @classmethod
    def recommend_mentors(
        cls,
        mentee_email: str,
        top_k: int = 5,
        db: Session | None = None,
    ) -> RecommendationListResponse[MentorRecommendationItem]:
        """
        Recomienda los Top-k mentores académicos más compatibles para un mentoreado.
        """
        clean_email = mentee_email.strip().lower()
        (
            mentee_courses,
            mentee_topics,
            mentee_slots,
            mentee_modality,
        ) = cls._get_mentee_profile_data(db, clean_email)

        candidates = cls.get_candidate_mentors(db)
        scored_items: list[tuple[float, float, int, int, str, MentorRecommendationItem]] = []

        for c in candidates:
            # Excluir al propio usuario si coincide el correo
            if c["email"].lower() == clean_email:
                continue

            cycle = c.get("ciclo_actual") or 1
            # Regla RN-03: Filtrar mentores con ciclo < 7
            if cycle < 7:
                continue

            c_courses = set(c.get("materias_interes") or [])
            c_topics = set(c.get("temas_seleccionados") or [])
            c_modality = c.get("modalidad_preferida") or "presencial"
            c_slots = {
                (s["dia_semana"], s["hora_inicio"], s["hora_fin"]) for s in (c.get("disponibilidad") or [])
            }

            score, breakdown = cls.compute_candidate_score(
                mentee_courses=mentee_courses,
                mentee_topics=mentee_topics,
                mentee_slots=mentee_slots,
                mentee_modality=mentee_modality,
                candidate_courses=c_courses,
                candidate_topics=c_topics,
                candidate_slots=c_slots,
                candidate_modality=c_modality,
                candidate_cycle=cycle,
            )

            # Extraer nombres de materias
            mat_nombres = [
                COURSE_METADATA.get(m_id, (f"CURSO-{m_id}", f"Asignatura {m_id}"))[1]
                for m_id in sorted(c_courses)
            ]

            item = MentorRecommendationItem(
                mentor_email=c["email"],
                mentor_codigo=c.get("codigo_estudiante"),
                mentor_nombres=c.get("nombres", "Mentor"),
                mentor_apellidos=c.get("apellidos", "EPIS"),
                mentor_ciclo=cycle,
                materias_ofrecidas=sorted(c_courses),
                materias_nombres=mat_nombres,
                temas_ofrecidos=sorted(c_topics),
                modalidad_preferida=c_modality,
                score_total=score,
                breakdown=breakdown,
            )

            # Criterio determinista de ordenamiento (score desc, weight desc, ciclo desc, slots desc, email asc)
            scored_items.append(
                (
                    -round(score, 4),
                    -round(breakdown.course_weight_factor, 2),
                    -cycle,
                    -breakdown.schedule_matching_slots_count,
                    c["email"],
                    item,
                )
            )

        scored_items.sort(key=lambda t: (t[0], t[1], t[2], t[3], t[4]))
        top_items = [t[5] for t in scored_items[:top_k]]

        return RecommendationListResponse(
            mentee_email=clean_email,
            total_candidates_evaluated=len(candidates),
            top_k=top_k,
            recommendations_count=len(top_items),
            items=top_items,
        )

    @classmethod
    def recommend_offers(
        cls,
        mentee_email: str,
        top_k: int = 5,
        id_asignatura: int | None = None,
        db: Session | None = None,
    ) -> RecommendationListResponse[OfferRecommendationItem]:
        """
        Recomienda las Top-k ofertas de mentoría programadas más compatibles con el mentoreado.
        """
        clean_email = mentee_email.strip().lower()
        (
            mentee_courses,
            mentee_topics,
            mentee_slots,
            mentee_modality,
        ) = cls._get_mentee_profile_data(db, clean_email)

        # Si se filtró por asignatura, ajustar cursos de interés
        if id_asignatura:
            mentee_courses = {id_asignatura}

        offers = OfferService.get_offers(db, id_asignatura=id_asignatura, estado="PUBLICADA")
        scored_offers: list[tuple[float, float, int, int, str, OfferRecommendationItem]] = []

        for off in offers:
            o_data = off.offer
            # Resolver fecha inicio
            iso_str = o_data.fecha_inicio.replace("Z", "+00:00")
            try:
                f_inicio = datetime.fromisoformat(iso_str)
                if f_inicio.tzinfo is None:
                    f_inicio = f_inicio.replace(tzinfo=UTC)
            except Exception:
                f_inicio = datetime.now(UTC)

            # Resolver ciclo del mentor
            mentor_profile = ProfileService.get_profile(db, o_data.mentor_email)
            mentor_cycle = mentor_profile.ciclo_actual
            if mentor_cycle < 7:
                # Regla RN-03
                continue

            c_courses = {o_data.id_asignatura}
            c_topics = {o_data.id_tema}
            c_modality = o_data.modalidad

            score, breakdown = cls.compute_candidate_score(
                mentee_courses=mentee_courses,
                mentee_topics=mentee_topics,
                mentee_slots=mentee_slots,
                mentee_modality=mentee_modality,
                candidate_courses=c_courses,
                candidate_topics=c_topics,
                candidate_slots=set(),
                candidate_modality=c_modality,
                candidate_cycle=mentor_cycle,
                offer_time=f_inicio,
                offer_duration_minutes=o_data.duracion_minutos,
            )

            rec_item = OfferRecommendationItem(
                id_oferta=off.id_oferta,
                codigo_sesion=off.codigo_sesion,
                id_asignatura=o_data.id_asignatura,
                codigo_asignatura=o_data.codigo_asignatura,
                nombre_asignatura=o_data.nombre_asignatura,
                id_tema=o_data.id_tema,
                nombre_tema=o_data.nombre_tema,
                fecha_inicio=o_data.fecha_inicio,
                duracion_minutos=o_data.duracion_minutos,
                modalidad=o_data.modalidad,
                aforo_maximo=o_data.aforo_maximo,
                espacio_asignado=o_data.espacio_asignado,
                mentor_email=o_data.mentor_email,
                mentor_nombre=o_data.mentor_nombre
                or f"{mentor_profile.nombres} {mentor_profile.apellidos}".strip(),
                mentor_ciclo=mentor_cycle,
                score_total=score,
                breakdown=breakdown,
            )

            scored_offers.append(
                (
                    -round(score, 4),
                    -round(breakdown.course_weight_factor, 2),
                    -mentor_cycle,
                    -breakdown.schedule_matching_slots_count,
                    off.codigo_sesion,
                    rec_item,
                )
            )

        scored_offers.sort(key=lambda t: (t[0], t[1], t[2], t[3], t[4]))
        top_items = [t[5] for t in scored_offers[:top_k]]

        return RecommendationListResponse(
            mentee_email=clean_email,
            total_candidates_evaluated=len(offers),
            top_k=top_k,
            recommendations_count=len(top_items),
            items=top_items,
        )

    @classmethod
    def explain_score(
        cls,
        mentee_email: str,
        mentor_email: str | None = None,
        id_oferta: str | None = None,
        db: Session | None = None,
    ) -> RecommendationExplainResponse:
        """
        Genera el desglose explicable institucional detallado de una recomendación.
        """
        clean_mentee = mentee_email.strip().lower()

        if mentor_email:
            clean_mentor = mentor_email.strip().lower()
            mentors = cls.recommend_mentors(clean_mentee, top_k=50, db=db)
            for m in mentors.items:
                if m.mentor_email.lower() == clean_mentor:
                    summary = (
                        f"El mentor {m.mentor_nombres} {m.mentor_apellidos} (Ciclo {m.mentor_ciclo}) "
                        f"alcanzó un puntaje EdRecSys de {m.score_total:.4f} debido a la compatibilidad temática "
                        f"(Jaccard {m.breakdown.topic_overlap_jaccard * 100:.1f}%), "
                        f"con {m.breakdown.schedule_matching_slots_count} franja(s) comunes y factor crítico {m.breakdown.course_weight_factor:.1f}x."
                    )
                    return RecommendationExplainResponse(
                        target_type="mentor",
                        target_id=clean_mentor,
                        mentee_email=clean_mentee,
                        score_total=m.score_total,
                        breakdown=m.breakdown,
                        institutional_summary=summary,
                    )
            # Si el mentor no estuvo en la lista de elegibles Top-k, verificar si realmente existe
            mentor_exists = False
            if db is not None:
                try:
                    p_db = db.query(PerfilAcademico).filter(PerfilAcademico.email == clean_mentor).first()
                    if p_db is not None:
                        mentor_exists = True
                except Exception:
                    pass

            if not mentor_exists:
                mem_p = get_profile_in_memory(clean_mentor)
                if mem_p is not None:
                    mentor_exists = True
                elif any(m["email"].lower() == clean_mentor for m in _DEFAULT_SYNTHETIC_MENTORS):
                    mentor_exists = True

            if not mentor_exists:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se encontró el mentor '{clean_mentor}' para generar el desglose explicable.",
                )

            # Si el mentor existe pero fue excluido (ej. ciclo < 7)
            mentor_profile = ProfileService.get_profile(db, clean_mentor)
            (
                m_courses,
                m_topics,
                m_slots,
                m_modality,
            ) = cls._get_mentee_profile_data(db, clean_mentee)

            cand_courses = set(mentor_profile.materias_interes or [])
            cand_topics = set(mentor_profile.temas_seleccionados or [])
            cand_modality = mentor_profile.modalidad_preferida or "presencial"
            cand_avail = ProfileService.get_availability(db, clean_mentor)
            cand_slots = {(s.dia_semana, s.hora_inicio, s.hora_fin) for s in (cand_avail or [])}

            score, breakdown = cls.compute_candidate_score(
                mentee_courses=m_courses,
                mentee_topics=m_topics,
                mentee_slots=m_slots,
                mentee_modality=m_modality,
                candidate_courses=cand_courses,
                candidate_topics=cand_topics,
                candidate_slots=cand_slots,
                candidate_modality=cand_modality,
                candidate_cycle=mentor_profile.ciclo_actual,
            )
            return RecommendationExplainResponse(
                target_type="mentor",
                target_id=clean_mentor,
                mentee_email=clean_mentee,
                score_total=score,
                breakdown=breakdown,
                institutional_summary="Evaluación directa de mentor. Verifique cumplimiento de requisitos institucionales RN-03.",
            )

        if id_oferta:
            offers_rec = cls.recommend_offers(clean_mentee, top_k=50, db=db)
            for off in offers_rec.items:
                if off.id_oferta == id_oferta or off.codigo_sesion == id_oferta:
                    summary = (
                        f"La sesión {off.codigo_sesion} de {off.nombre_asignatura} - {off.nombre_tema} "
                        f"alcanzó un puntaje EdRecSys de {off.score_total:.4f}. "
                        f"Modalidad {off.modalidad} con aforo reglamentario de {off.aforo_maximo} estudiantes."
                    )
                    return RecommendationExplainResponse(
                        target_type="offer",
                        target_id=id_oferta,
                        mentee_email=clean_mentee,
                        score_total=off.score_total,
                        breakdown=off.breakdown,
                        institutional_summary=summary,
                    )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró el mentor u oferta especificada para generar el desglose explicable.",
        )
