import z from "zod";

export const datoHistograma = z.object({
  calificacion: z.number(),
  qty: z.number()
})

export const datoPareto = z.object({
  factor: z.string(),
  qty: z.number()
})

export const datoDispersion = z.object({
  calificacion: z.number(),
  faltas: z.number()
})

export const datoControl = z.object({
  unidad: z.number(),
  calificacionPromedio: z.number()
})

export type DatoHistograma = z.infer<typeof datoHistograma>
export type DatoPareto = z.infer<typeof datoPareto>
export type DatoDispersion = z.infer<typeof datoDispersion>
export type DatoControl = z.infer<typeof datoControl>
