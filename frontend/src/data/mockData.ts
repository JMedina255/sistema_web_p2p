// Datos mock actualizados para la maqueta del Sistema Web P2P (EPIS-UPT, 2026)
// Enfoque simplificado, directo y con buscador dinámico por escritura

export interface CarouselSlide {
  id: string;
  image: string;
  tag: string;
  title: string;
  subtitle: string;
}

export interface Subject {
  id: string;
  name: string;
  code: string;
  cycle: string;
  category: string;
  description: string;
  topics: string[];
}

export interface Mentor {
  id: string;
  name: string;
  cycle: string;
  code: string;
  email: string;
  avatar: string;
  subjectSpecialties: string[];
  gradeInSubject: number;
  totalHours: number;
  rating: number;
  reviewsCount: number;
  badges: string[];
  availabilitySlots: {
    day: string;
    time: string;
    id: string;
    available: boolean;
  }[];
  affinityPercentage?: number;
}

export interface AvailableMentorship {
  id: string;
  subjectName: string;
  subjectCode: string;
  cycle: string;
  topic: string;
  mentor: Mentor;
  scheduleDay: string;
  scheduleTime: string;
  modality: string;
  slotId: string;
}

export interface SessionBooking {
  id: string;
  mentorName: string;
  studentName: string;
  studentCode?: string;
  subjectName: string;
  topic: string;
  day: string;
  time: string;
  status: 'PENDIENTE' | 'CONFIRMADA' | 'QUORUM_INSUFICIENTE' | 'CONFIRMADA_EXCEPCIONAL' | 'CANCELADA_QUORUM' | 'EN_CURSO' | 'COMPLETADA';
  dateFormatted: string;
  modality?: string;
  enrolledStudentsCount?: number;
  minQuorumRequired?: number; // RN-09: 50%
  ratifiedT24?: boolean;
  qrToken?: string;
  qrScanned?: boolean;
}

// 1. Carrusel de Imágenes Institucional
export const HERO_SLIDES: CarouselSlide[] = [
  {
    id: 'slide-1',
    image: 'https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=1400&auto=format&fit=crop&q=80',
    tag: 'Red de Mentorías EPIS UPT',
    title: 'Aprende de estudiante a estudiante',
    subtitle: 'Refuerzo personalizado en asignaturas críticas de la carrera.'
  },
  {
    id: 'slide-2',
    image: 'https://images.unsplash.com/photo-1531482615713-2afd69097998?w=1400&auto=format&fit=crop&q=80',
    tag: 'Emparejamiento Inteligente',
    title: 'Encuentra al mentor ideal para tu tema',
    subtitle: 'Búsqueda directa por materia, tema de interés y horarios compatibles.'
  },
  {
    id: 'slide-3',
    image: 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=1400&auto=format&fit=crop&q=80',
    tag: 'Convalidación Oficial',
    title: 'Acreditación de horas para mentores',
    subtitle: 'Horas extracurriculares reconocidas ante la Dirección de Escuela.'
  }
];

// 2. Asignaturas Disponibles
export const CRITICAL_SUBJECTS: Subject[] = [
  {
    id: 'sub-01',
    name: 'Algoritmos y Estructura de Datos',
    code: 'SI-301',
    cycle: 'III Ciclo',
    category: 'Programación',
    description: 'Punteros, memoria dinámica, recursión, árboles y grafos.',
    topics: ['Recursividad', 'Punteros C++', 'Árboles Binarios', 'Grafos']
  },
  {
    id: 'sub-02',
    name: 'Cálculo I',
    code: 'CB-101',
    cycle: 'I Ciclo',
    category: 'Ciencias Básicas',
    description: 'Límites, continuidad y cálculo diferencial.',
    topics: ['Límites', 'Derivadas', 'Optimización', 'Regla de la Cadena']
  },
  {
    id: 'sub-03',
    name: 'Programación Orientada a Objetos',
    code: 'SI-202',
    cycle: 'II Ciclo',
    category: 'Programación',
    description: 'Clases, herencia, polimorfismo y patrones.',
    topics: ['Herencia', 'Polimorfismo', 'Interfaces Java', 'Patrones de Diseño']
  },
  {
    id: 'sub-04',
    name: 'Base de Datos I',
    code: 'SI-402',
    cycle: 'IV Ciclo',
    category: 'Ingeniería de Datos',
    description: 'Modelado relacional, SQL y normalización.',
    topics: ['Normalización 3FN', 'Consultas JOIN', 'Triggers', 'Álgebra Relacional']
  },
  {
    id: 'sub-05',
    name: 'Cálculo II',
    code: 'CB-201',
    cycle: 'II Ciclo',
    category: 'Ciencias Básicas',
    description: 'Integrales indefinidas, definidas y series.',
    topics: ['Integrales por Partes', 'Fracciones Parciales', 'Series de Taylor']
  }
];

// 3. Mentores
export const MOCK_MENTORS: Mentor[] = [
  {
    id: 'm-01',
    name: 'Renzo Antonio Antayhua',
    cycle: 'IX Ciclo EPIS',
    code: '2022073504',
    email: 'rantayhua@upt.pe',
    avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=200&auto=format&fit=crop&q=80',
    subjectSpecialties: ['Algoritmos y Estructura de Datos', 'Programación Orientada a Objetos'],
    gradeInSubject: 18.5,
    totalHours: 32,
    rating: 4.9,
    reviewsCount: 28,
    badges: ['Top Mentor EPIS', 'Mentor Oro'],
    availabilitySlots: [
      { id: 'slot-1', day: 'Viernes', time: '10:00 - 11:30', available: true },
      { id: 'slot-2', day: 'Miércoles', time: '18:00 - 19:30', available: true }
    ]
  },
  {
    id: 'm-02',
    name: 'Joan Medina Q',
    cycle: 'VIII Ciclo EPIS',
    code: '2022074255',
    email: 'jmedina@upt.pe',
    avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&auto=format&fit=crop&q=80',
    subjectSpecialties: ['Cálculo I', 'Cálculo II', 'Base de Datos I'],
    gradeInSubject: 19.0,
    totalHours: 26,
    rating: 4.8,
    reviewsCount: 22,
    badges: ['Mentor Plata', 'Acreditado EPIS'],
    availabilitySlots: [
      { id: 'slot-3', day: 'Jueves', time: '17:00 - 18:30', available: true },
      { id: 'slot-4', day: 'Martes', time: '15:00 - 16:30', available: true }
    ]
  },
  {
    id: 'm-03',
    name: 'Camila Valeria Ramos',
    cycle: 'VII Ciclo EPIS',
    code: '2023019842',
    email: 'cramos@upt.pe',
    avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=200&auto=format&fit=crop&q=80',
    subjectSpecialties: ['Programación Orientada a Objetos', 'Cálculo I'],
    gradeInSubject: 17.8,
    totalHours: 18,
    rating: 4.75,
    reviewsCount: 16,
    badges: ['Mentor Bronce', 'Pedagogía Clara'],
    availabilitySlots: [
      { id: 'slot-5', day: 'Lunes', time: '14:00 - 15:30', available: true },
      { id: 'slot-6', day: 'Sábado', time: '10:00 - 11:30', available: true }
    ]
  }
];

// 4. Catálogo Completo de Mentorías Disponibles para Búsqueda Directa
export const AVAILABLE_MENTORSHIPS: AvailableMentorship[] = [
  {
    id: 'ment-1',
    subjectName: 'Algoritmos y Estructura de Datos',
    subjectCode: 'SI-301',
    cycle: 'III Ciclo',
    topic: 'Recursividad y Punteros en C++',
    mentor: MOCK_MENTORS[0],
    scheduleDay: 'Viernes',
    scheduleTime: '10:00 - 11:30 AM',
    modality: 'Presencial (Lab EPIS 2)',
    slotId: 'slot-1'
  },
  {
    id: 'ment-2',
    subjectName: 'Algoritmos y Estructura de Datos',
    subjectCode: 'SI-301',
    cycle: 'III Ciclo',
    topic: 'Árboles Binarios AVL y Grafos',
    mentor: MOCK_MENTORS[0],
    scheduleDay: 'Miércoles',
    scheduleTime: '06:00 - 07:30 PM',
    modality: 'Virtual (Google Meet)',
    slotId: 'slot-2'
  },
  {
    id: 'ment-3',
    subjectName: 'Cálculo I',
    subjectCode: 'CB-101',
    cycle: 'I Ciclo',
    topic: 'Límites Indeterminados y Asíntotas',
    mentor: MOCK_MENTORS[1],
    scheduleDay: 'Jueves',
    scheduleTime: '05:00 - 06:30 PM',
    modality: 'Virtual (Google Meet)',
    slotId: 'slot-3'
  },
  {
    id: 'ment-4',
    subjectName: 'Cálculo I',
    subjectCode: 'CB-101',
    cycle: 'I Ciclo',
    topic: 'Derivadas Implícitas y Optimización',
    mentor: MOCK_MENTORS[2],
    scheduleDay: 'Lunes',
    scheduleTime: '02:00 - 03:30 PM',
    modality: 'Presencial (Lab EPIS 1)',
    slotId: 'slot-5'
  },
  {
    id: 'ment-5',
    subjectName: 'Programación Orientada a Objetos',
    subjectCode: 'SI-202',
    cycle: 'II Ciclo',
    topic: 'Polimorfismo, Interfaces y Clases Abstractas en Java',
    mentor: MOCK_MENTORS[2],
    scheduleDay: 'Sábado',
    scheduleTime: '10:00 - 11:30 AM',
    modality: 'Virtual (Google Meet)',
    slotId: 'slot-6'
  },
  {
    id: 'ment-6',
    subjectName: 'Programación Orientada a Objetos',
    subjectCode: 'SI-202',
    cycle: 'II Ciclo',
    topic: 'Patrones de Diseño de Software (Singleton / Factory)',
    mentor: MOCK_MENTORS[0],
    scheduleDay: 'Viernes',
    scheduleTime: '10:00 - 11:30 AM',
    modality: 'Presencial (Lab EPIS 2)',
    slotId: 'slot-1'
  },
  {
    id: 'ment-7',
    subjectName: 'Base de Datos I',
    subjectCode: 'SI-402',
    cycle: 'IV Ciclo',
    topic: 'Normalización hasta 3FN y Consultas SQL con JOIN',
    mentor: MOCK_MENTORS[1],
    scheduleDay: 'Martes',
    scheduleTime: '03:00 - 04:30 PM',
    modality: 'Presencial (Lab Base de Datos)',
    slotId: 'slot-4'
  },
  {
    id: 'ment-8',
    subjectName: 'Base de Datos I',
    subjectCode: 'SI-402',
    cycle: 'IV Ciclo',
    topic: 'Triggers, Procedimientos Almacenados y Vistas SQL',
    mentor: MOCK_MENTORS[1],
    scheduleDay: 'Jueves',
    scheduleTime: '05:00 - 06:30 PM',
    modality: 'Virtual (Google Meet)',
    slotId: 'slot-3'
  },
  {
    id: 'ment-9',
    subjectName: 'Cálculo II',
    subjectCode: 'CB-201',
    cycle: 'II Ciclo',
    topic: 'Técnicas de Integración por Partes y Fracciones Parciales',
    mentor: MOCK_MENTORS[1],
    scheduleDay: 'Jueves',
    scheduleTime: '05:00 - 06:30 PM',
    modality: 'Virtual (Google Meet)',
    slotId: 'slot-3'
  },
  {
    id: 'ment-10',
    subjectName: 'Cálculo II',
    subjectCode: 'CB-201',
    cycle: 'II Ciclo',
    topic: 'Series de Potencias y Polinomios de Taylor',
    mentor: MOCK_MENTORS[1],
    scheduleDay: 'Martes',
    scheduleTime: '03:00 - 04:30 PM',
    modality: 'Virtual (Google Meet)',
    slotId: 'slot-4'
  }
];

// 5. Sesiones Iniciales de Prueba
export const INITIAL_BOOKINGS: SessionBooking[] = [
  {
    id: 'ses-101',
    mentorName: 'Joan Medina Q',
    studentName: 'Renzo Antayhua M (II Ciclo)',
    studentCode: '2025018341',
    subjectName: 'Algoritmos y Estructura de Datos',
    topic: 'Recursividad y Memoria Dinámica en C++',
    day: 'Viernes',
    time: '10:00 - 11:30 AM',
    status: 'CONFIRMADA',
    dateFormatted: 'Viernes 10 Octubre, 10:00 AM',
    modality: 'Presencial (Lab EPIS 2)',
    enrolledStudentsCount: 5,
    minQuorumRequired: 3,
    ratifiedT24: true,
    qrToken: 'QR-P2P-SI301-2025018341-998',
    qrScanned: true
  },
  {
    id: 'ses-102',
    mentorName: 'Joan Medina Q',
    studentName: 'Renzo Antayhua M (II Ciclo)',
    studentCode: '2025018341',
    subjectName: 'Cálculo I',
    topic: 'Límites Indeterminados y Asíntotas',
    day: 'Jueves',
    time: '05:00 - 06:30 PM',
    status: 'PENDIENTE',
    dateFormatted: 'Jueves 16 Octubre, 05:00 PM',
    modality: 'Virtual (Google Meet)',
    enrolledStudentsCount: 3,
    minQuorumRequired: 3,
    ratifiedT24: false,
    qrToken: 'QR-P2P-CB101-2025018341-452',
    qrScanned: false
  },
  {
    id: 'ses-103',
    mentorName: 'Joan Medina Q',
    studentName: 'Ana Sofía Ticona (I Ciclo)',
    studentCode: '2025019012',
    subjectName: 'Base de Datos I',
    topic: 'Normalización 3FN y Consultas SQL con JOIN',
    day: 'Martes',
    time: '03:00 - 04:30 PM',
    status: 'QUORUM_INSUFICIENTE',
    dateFormatted: 'Martes 14 Octubre, 03:00 PM',
    modality: 'Presencial (Lab BD)',
    enrolledStudentsCount: 1,
    minQuorumRequired: 3,
    ratifiedT24: false,
    qrToken: 'QR-P2P-SI402-2025019012-103',
    qrScanned: false
  },
  {
    id: 'ses-104',
    mentorName: 'Joan Medina Q',
    studentName: 'Carlos Paredes (II Ciclo)',
    studentCode: '2024017721',
    subjectName: 'Cálculo II',
    topic: 'Integrales por Partes y Fracciones Parciales',
    day: 'Jueves',
    time: '05:00 - 06:30 PM',
    status: 'COMPLETADA',
    dateFormatted: 'Ayer, 05:00 PM',
    modality: 'Virtual (Google Meet)',
    enrolledStudentsCount: 4,
    minQuorumRequired: 2,
    ratifiedT24: true,
    qrToken: 'QR-P2P-CB201-2024017721-776',
    qrScanned: true
  }
];

// 6. Insignias
export const GAMIFICATION_BADGES = [
  {
    name: 'Top Mentor EPIS',
    icon: '👑',
    desc: 'Mayor cantidad de sesiones con calificación 5.0.',
    unlocked: true
  },
  {
    name: 'Mentor Oro (30+ Horas)',
    icon: '🥇',
    desc: 'Más de 30 horas acreditadas ante la Dirección EPIS.',
    unlocked: true
  },
  {
    name: 'Mentor Plata (20+ Horas)',
    icon: '🥈',
    desc: 'Más de 20 horas efectivas de asesoría entre pares.',
    unlocked: true
  },
  {
    name: '100% Puntualidad',
    icon: '🎯',
    desc: 'Asistencia perfecta en todas las sesiones agendadas.',
    unlocked: true
  }
];

// 7. Cuentas y Credenciales de Usuario Institucional (CUS01 / RF02)
export type UserRole = 'admin' | 'mentor' | 'mentee';

export interface UserAccount {
  username: string;
  password: string;
  role: UserRole;
  name: string;
  title: string;
  code: string;
  email: string;
  avatar: string;
  cycle?: string;
  hasAcceptedConsent: boolean;
}

export const MOCK_USERS: UserAccount[] = [
  {
    username: 'admin',
    password: 'admin123',
    role: 'admin',
    name: 'Ing. Liliana Vega Bernal',
    title: 'Comité de Tutoría EPIS-UPT',
    code: 'DOC-EPIS-018',
    email: 'lvega@upt.pe',
    avatar: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=200&auto=format&fit=crop&q=80',
    hasAcceptedConsent: true
  },
  {
    username: 'mentor',
    password: 'mentor123',
    role: 'mentor',
    name: 'Joan Medina Q',
    title: 'Mentor Académico • VIII Ciclo',
    code: '2022074255',
    cycle: 'VIII Ciclo EPIS',
    email: 'jmedina@upt.pe',
    avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&auto=format&fit=crop&q=80',
    hasAcceptedConsent: true
  },
  {
    username: 'mentoreado',
    password: 'mentoreado123',
    role: 'mentee',
    name: 'Renzo Antayhua M',
    title: 'Estudiante Mentoreado • II Ciclo',
    code: '2025018341',
    cycle: 'II Ciclo EPIS',
    email: 'rantayhua@upt.pe',
    avatar: 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=200&auto=format&fit=crop&q=80',
    hasAcceptedConsent: false
  }
];

// 8. Bitácoras Pedagógicas Docentes (CUS10 / CUS22 / RN-12 / RN-14)
export interface PedagogicalLog {
  id: string;
  sessionId: string;
  mentorName: string;
  mentorCode: string;
  subjectName: string;
  topic: string;
  date: string;
  durationHours: number;
  studentsAttended: string[];
  summary: string;
  observations: string;
  status: 'BORRADOR' | 'REGISTRADA' | 'VISADA' | 'OBSERVADA';
  auditFeedback?: string;
  auditDate?: string;
  hashSha256?: string;
}

export const INITIAL_LOGS: PedagogicalLog[] = [
  {
    id: 'log-001',
    sessionId: 'ses-102',
    mentorName: 'Joan Medina Q',
    mentorCode: '2022074255',
    subjectName: 'Cálculo I',
    topic: 'Límites Indeterminados 0/0 y Factorización Racional',
    date: '02 Oct 2026',
    durationHours: 2.0,
    studentsAttended: ['Renzo Antayhua M (2025018341)', 'Ana Sofía Ticona (2025019012)'],
    summary: 'Se reforzó la regla de L\'Hôpital y la racionalización con raíces cúbicas. Los estudiantes resolvieron 4 ejercicios tipo examen parcial.',
    observations: 'Excelente participación activa y resolución en pizarra virtual.',
    status: 'REGISTRADA'
  },
  {
    id: 'log-002',
    sessionId: 'ses-101',
    mentorName: 'Joan Medina Q',
    mentorCode: '2022074255',
    subjectName: 'Algoritmos y Estructura de Datos',
    topic: 'Recursividad en Árboles Binarios AVL',
    date: '28 Sep 2026',
    durationHours: 2.5,
    studentsAttended: ['Renzo Antayhua M (2025018341)', 'Diego Flores (2024016633)'],
    summary: 'Implementación del balanceo y rotaciones simples y dobles en C++ con verificación en depurador.',
    observations: 'Se dejó repositorio con pruebas unitarias en Google Classroom.',
    status: 'VISADA',
    auditFeedback: 'Cumple a cabalidad con la trazabilidad pedagógica. Horas validadas oficialmente.',
    auditDate: '30 Sep 2026',
    hashSha256: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
  },
  {
    id: 'log-003',
    sessionId: 'ses-97',
    mentorName: 'Camila Valeria Ramos',
    mentorCode: '2023019842',
    subjectName: 'Programación Orientada a Objetos',
    topic: 'Polimorfismo e Interfaces en Java',
    date: '25 Sep 2026',
    durationHours: 1.5,
    studentsAttended: ['Valeria Choque (2025018899)'],
    summary: 'Diferenciación entre clases abstractas e interfaces con ejemplos prácticos de arquitectura en capas.',
    observations: 'Sesión presencial realizada en Lab EPIS 1.',
    status: 'VISADA',
    auditFeedback: 'Validado satisfactoriamente por Comité de Tutoría EPIS.',
    auditDate: '27 Sep 2026',
    hashSha256: '4f8b2d1c9a6e3f5b8d7a1c0e2f4a6b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a'
  }
];

// 9. Certificados Digitales Foliados con Hash SHA-256 (CUS13 / CUS09 / RN-14)
export interface DigitalCertificate {
  folio: string;
  mentorName: string;
  mentorCode: string;
  hoursValidated: number;
  issueDate: string;
  semester: string;
  hashSha256: string;
  qrVerificationUrl: string;
  signedBy: string;
}

export const INITIAL_CERTIFICATES: DigitalCertificate[] = [
  {
    folio: 'CERT-EPIS-2026-089',
    mentorName: 'Joan Medina Q',
    mentorCode: '2022074255',
    hoursValidated: 26,
    issueDate: '01 Octubre 2026',
    semester: 'Semestre Académico 2026-II',
    hashSha256: '9f83c6b2d1e4a7c8b0e3f5a2c4d6e8b0a1c3e5f7a9b2d4e6f8a0c2e4b6d8f0a2',
    qrVerificationUrl: 'https://epis.upt.edu.pe/verificar/CERT-EPIS-2026-089',
    signedBy: 'Ing. Liliana Vega Bernal — Comité de Tutoría EPIS'
  }
];

// 10. Solicitudes Temáticas por Demanda (CUS03 / RF04)
export interface DemandRequest {
  id: string;
  studentName: string;
  studentCode: string;
  cycle: string;
  subjectName: string;
  topicNeeded: string;
  description: string;
  preferredModality: string;
  dateCreated: string;
  status: 'ABIERTA' | 'ATENDIDA';
}

export const INITIAL_DEMAND_REQUESTS: DemandRequest[] = [
  {
    id: 'req-01',
    studentName: 'Renzo Antayhua M',
    studentCode: '2025018341',
    cycle: 'II Ciclo',
    subjectName: 'Programación Orientada a Objetos',
    topicNeeded: 'Patrón Singleton y Factory en Java',
    description: 'Tengo dificultades para estructurar las instancias en el proyecto semestral.',
    preferredModality: 'Virtual (Meet)',
    dateCreated: '04 Oct 2026',
    status: 'ABIERTA'
  },
  {
    id: 'req-02',
    studentName: 'Mariana Condori',
    studentCode: '2025019801',
    cycle: 'I Ciclo',
    subjectName: 'Cálculo I',
    topicNeeded: 'Optimización de funciones y máximos/mínimos',
    description: 'Problemas de aplicación geométrica en optimización de áreas y volúmenes.',
    preferredModality: 'Presencial (Lab EPIS 1)',
    dateCreated: '03 Oct 2026',
    status: 'ABIERTA'
  }
];

// 11. Ponderación Curricular Directiva (CUS12 / RN-11)
export interface SubjectPriority {
  id: string;
  subjectName: string;
  criticalFactorAlpha: number; // α entre 1.05 y 1.50 (RN-11)
  isPriorityBoosted: boolean;
  failRateEstimated: number;
}

export const INITIAL_SUBJECT_PRIORITIES: SubjectPriority[] = [
  { id: 'sub-01', subjectName: 'Algoritmos y Estructura de Datos', criticalFactorAlpha: 1.35, isPriorityBoosted: true, failRateEstimated: 41 },
  { id: 'sub-02', subjectName: 'Cálculo I', criticalFactorAlpha: 1.50, isPriorityBoosted: true, failRateEstimated: 46 },
  { id: 'sub-03', subjectName: 'Programación Orientada a Objetos', criticalFactorAlpha: 1.25, isPriorityBoosted: true, failRateEstimated: 32 },
  { id: 'sub-04', subjectName: 'Base de Datos I', criticalFactorAlpha: 1.20, isPriorityBoosted: true, failRateEstimated: 28 },
  { id: 'sub-05', subjectName: 'Cálculo II', criticalFactorAlpha: 1.45, isPriorityBoosted: true, failRateEstimated: 44 }
];
