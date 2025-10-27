import { z } from 'zod';
import { alumnoSchema } from './alumnoSchema';

const calificacionSchema = z.object({
	unidad: z.number().int().min(1),
	calificacion: z.number().min(0).max(100),
	faltas: z.number().int().min(0)
});

const inscripcionSchema = z.object({
	grupo: z.string().min(1),
	nombreMateria: z.string().min(1),
	serieMateria: z.string().min(1),
	calificaciones: calificacionSchema.array()
});

export const alumnoDetalleSchema = alumnoSchema.extend({
	genero: z.string().min(1),
	estado: z.string().min(1),
	semestre: z.number().int().min(1),
	nombreCarrera: z.string().min(1),
	modalidadCarrera: z.string().min(1),
	inscripciones: inscripcionSchema.array(),
	fotoUrl: z.string().url().optional()
});

export type AlumnoDetalle = z.infer<typeof alumnoDetalleSchema>;

