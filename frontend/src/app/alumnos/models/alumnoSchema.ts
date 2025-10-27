import { z } from 'zod';

export const alumnoSchema = z.object({
	numeroDeControl: z.string().min(1, 'El numero de control es obligatorio'),
	nombre: z.string().min(1, 'El nombre es obligatorio'),
	apellidoPaterno: z.string().min(1, 'El apellido paterno es obligatorio'),
	apellidoMaterno: z.string().nullable(),
	factoresDeRiesgo: z.string().min(1).array()
});

export type Alumno = z.infer<typeof alumnoSchema>;
