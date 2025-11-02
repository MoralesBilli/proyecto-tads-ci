import { Injectable, signal } from '@angular/core';
import { httpResource } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { auditTrailSchema } from '../models/auditTrailSchema';

@Injectable({ providedIn: 'root' })
export class AuditTrailService {
  private readonly apiUrl = environment.apiUrl;
  readonly emptyMessage = signal<string | null>(null);

  readonly logs = httpResource(
    () => `${this.apiUrl}/logs`,
    {
      parse: (data: unknown) => {
        if (data && typeof data === 'object' && 'mensaje' in (data as any)) {
          const msg = (data as any).mensaje;
          this.emptyMessage.set(typeof msg === 'string' ? msg : '');
          return [];
        }
        this.emptyMessage.set(null);
        return auditTrailSchema.array().parse(data);
      },
      defaultValue: [],
    }
  );
}
