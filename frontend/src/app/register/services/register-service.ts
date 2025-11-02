import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';
import { firstValueFrom } from 'rxjs';

export interface RegisterPayload {
  nombre: string;
  apellidopa: string;
  apellidoma?: string;
  telefono?: string;
  correo?: string;
  clave: string | number; // clave maestro / número de empleado
}

@Injectable({
  providedIn: 'root'
})
export class RegisterService {
  private readonly apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  register(payload: RegisterPayload) {
    const url = `${this.apiUrl}/crear-usuario`;
    const form = new FormData();
    form.append('clave', String(payload.clave));
    form.append('nombre', payload.nombre);
    form.append('apellidopa', payload.apellidopa);
    if (payload.apellidoma) form.append('apellidoma', payload.apellidoma);
    if (payload.telefono) form.append('telefono', payload.telefono);
    if (payload.correo) form.append('correo', payload.correo);
    return firstValueFrom(this.http.post(url, form));
  }
}
