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
  subjectName: string;
  topic: string;
  day: string;
  time: string;
  status: 'PENDIENTE' | 'CONFIRMADA' | 'COMPLETADA';
  dateFormatted: string;
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
    name: 'Joan Cristian Medina',
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
    mentorName: 'Renzo Antonio Antayhua',
    studentName: 'Lucas Mamani (II Ciclo)',
    subjectName: 'Algoritmos y Estructura de Datos',
    topic: 'Recursividad y Memoria Dinámica en C++',
    day: 'Viernes',
    time: '10:00 - 11:30 AM',
    status: 'CONFIRMADA',
    dateFormatted: '12 Sep 2026, 10:00 AM'
  },
  {
    id: 'ses-102',
    mentorName: 'Joan Cristian Medina',
    studentName: 'Ana Sofía Ticona (I Ciclo)',
    subjectName: 'Cálculo I',
    topic: 'Límites Indeterminados',
    day: 'Jueves',
    time: '05:00 - 06:30 PM',
    status: 'PENDIENTE',
    dateFormatted: '11 Sep 2026, 05:00 PM'
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
