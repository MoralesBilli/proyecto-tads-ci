import { z } from 'zod';

export const auditTrailSchema = z.object({
  id: z.number(),
  accion: z.string(),
  clave_docente: z.number(),
  create_at: z.string(),
  origin: z.string(),
});

export type AuditTrail = z.infer<typeof auditTrailSchema>;
