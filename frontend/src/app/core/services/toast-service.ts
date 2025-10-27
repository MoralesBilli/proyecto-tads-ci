import { Injectable, signal } from '@angular/core';

export type ToastType = 'success' | 'error' | 'info' | 'warning';

export interface Toast {
  id: number;
  message: string;
  type: ToastType;
  duration?: number; // ms
}

@Injectable({
  providedIn: 'root'
})
export class ToastService {
  toasts = signal<Toast[]>([]);
  #id = 0;

  show(message: string, type: ToastType = 'info', duration = 3000) {
    const id = this.#id++;
    this.toasts.update(list => [...list, { id, message, type, duration }]);

    // auto-cerrar
    const timer = setTimeout(() => this.dismiss(id), duration);
    // (opcional) guarda el timer si quisieras pausar con hover
    return id;
  }

  dismiss(id: number) {
    this.toasts.update(list => list.filter(t => t.id !== id));
  }

  clear() {
    this.toasts.set([]);
  }
}
