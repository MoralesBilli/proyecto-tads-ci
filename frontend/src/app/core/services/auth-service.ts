import { Injectable, computed, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { firstValueFrom } from 'rxjs';

export type JwtResponse = { token?: string; jwt?: string; access_token?: string; acceso?: boolean; message?: string } & Record<string, unknown>;
export interface JwtPayload { id?: number; doce?: number; exp?: number }

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly storageKey = 'auth.jwt';
  private readonly apiUrl = environment.apiUrl;

  private readonly _token = signal<string | null>(this.loadToken());
  readonly token = this._token.asReadonly();
  readonly isAuthenticated = computed(() => !!this._token());
  readonly decoded = computed<JwtPayload | null>(() => {
    const t = this._token();
    if (!t) return null as null | Record<string, any>;
    const parts = t.split('.');
    if (parts.length !== 3) return null;
    try {
      const payload = JSON.parse(atob(parts[1]));
      return payload as JwtPayload;
    } catch {
      return null;
    }
  });

  constructor(private http: HttpClient) {}

  private loadToken(): string | null {
    try { return localStorage.getItem(this.storageKey); } catch { return null; }
  }

  private persistToken(token: string | null) {
    try {
      if (token) localStorage.setItem(this.storageKey, token);
      else localStorage.removeItem(this.storageKey);
    } catch { /* ignore */ }
  }

  setToken(token: string | null) {
    this._token.set(token);
    this.persistToken(token);
  }

  async login(params: { user: string | number; password: string }) {
    const url = `${this.apiUrl}/inicio_sesion`;
    const res = await firstValueFrom(this.http.post<JwtResponse>(url, params));
    const token = res?.token || res?.jwt || res?.access_token;
    if (!token) throw new Error('No se recibió token');
    this.setToken(String(token));
    return res;
  }

  changePassword(body: { contrasena_actual: string; nueva_contrasena: string }) {
    const url = `${this.apiUrl}/cambiar-contraseña`;
    return firstValueFrom(this.http.put(url, body));
  }

  logout() {
    this.setToken(null);
  }
}
