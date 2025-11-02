import { ChangeDetectionStrategy, Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { RegisterService } from '../services/register-service';
import { ToastService } from '../../core/services/toast-service';
import { LayoutService } from '../../core/services/layout-service';

@Component({
  selector: 'app-register-page',
  imports: [ReactiveFormsModule, CommonModule, RouterModule],
  templateUrl: './register-page.html',
  styleUrl: './register-page.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class RegisterPage {
  private fb = new FormBuilder();
  private readonly layout = inject(LayoutService);

  form = this.fb.group({
    nombre: ['', [Validators.required]],
    apellidopa: ['', [Validators.required]],
    apellidoma: ['', [Validators.required]],
    telefono: ['', [Validators.required, Validators.pattern(/^\+?[0-9\s-]{7,20}$/)]],
    correo: ['', [Validators.required, Validators.email]],
    clave: ['', [Validators.required, Validators.pattern(/^[0-9]+$/)]],
  });

  loading = signal(false);
  error = signal<string | null>(null);

  constructor(private svc: RegisterService, private toast: ToastService, private router: Router) {
    this.layout.title.set('Registro');
  }

  async submit() {
    if (this.form.invalid) return this.form.markAllAsTouched();
    const payload = this.form.value as any;

    this.loading.set(true); this.error.set(null);
    try {
      const res = await this.svc.register(payload);
      const msg = (res as any)?.message || (res as any)?.mensaje || 'Cuenta creada. Ahora puedes iniciar sesión';
      this.toast.show(msg, 'success', 4000);
      await this.router.navigateByUrl('/login');
    } catch (err: any) {
      const message = err?.error?.error || err?.error?.message || err?.message || 'Error al registrar';
      this.toast.show(message, 'error', 5000);
      this.error.set(null);
    } finally { this.loading.set(false); }
  }
}
