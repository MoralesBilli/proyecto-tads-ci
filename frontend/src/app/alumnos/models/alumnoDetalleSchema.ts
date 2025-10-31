import { z } from 'zod';

const calificacionSchema = z.object({
	unidad: z.number().int().min(0, 'La unidad debe ser positiva'),
	calificacion: z.number().int().min(0, 'La calificación no puede ser negativa').max(100, 'La calificación no puede exceder 100'),
	faltas: z.number().int().min(0, 'Las faltas no pueden ser negativas')
});

const inscripcionSchema = z.object({
	grupo: z.string().min(1, 'El grupo es obligatorio'),
	nombreMateria: z.string().min(1, 'El nombre de la materia es obligatorio'),
	serieMateria: z.string().min(1, 'La serie de la materia es obligatoria'),
	calificaciones: calificacionSchema.array()
});

export const alumnoDetalleSchema = z.object({
	numeroDeControl: z.string().min(1, 'El número de control es obligatorio'),
	nombre: z.string().min(1, 'El nombre es obligatorio'),
	apellidoPaterno: z.string().min(1, 'El apellido paterno es obligatorio'),
	apellidoMaterno: z.string().min(1, 'El apellido materno es obligatorio'),
	genero: z.string().min(1, 'El género es obligatorio'),
	estado: z.string().min(1, 'El estado es obligatorio'),
	modalidadCarrera: z.string().min(1, 'La modalidad de la carrera es obligatoria'),
	nombreCarrera: z.string().min(1, 'El nombre de la carrera es obligatorio'),
	semestre: z.string().min(1, 'El semestre es obligatorio'),
	factoresDeRiesgo: z.string().array(),
	inscripciones: inscripcionSchema.array()
});

export type AlumnoDetalle = z.infer<typeof alumnoDetalleSchema>;
