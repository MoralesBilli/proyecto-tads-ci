import { ChangeDetectionStrategy, Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../core/services/auth-service';
import { LayoutService } from '../../core/services/layout-service';
import { ToastService } from '../../core/services/toast-service';

@Component({
  selector: 'app-login-page',
  imports: [ReactiveFormsModule, CommonModule, RouterLink],
  templateUrl: './login-page.html',
  styleUrl: './login-page.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LoginPage {
  private fb = new FormBuilder();
  private readonly layout = inject(LayoutService);

  form = this.fb.group({
    clave: ['', [Validators.required, Validators.pattern(/^[0-9]+$/)]],
    password: ['', [Validators.required]],
  });

  loading = signal(false);
  error = signal<string | null>(null);

  constructor(private svc: AuthService, private router: Router, private toast: ToastService) {
    this.layout.title.set('Iniciar sesión');
  }

  async submit() {
    if (this.form.invalid) return this.form.markAllAsTouched();
    this.loading.set(true);
    this.error.set(null);
    try {
  const { clave, password } = this.form.value as any;
  const res = await this.svc.login({ user: clave, password });
      const firstTime = Boolean((res as any)?.acceso);
      if (firstTime) {
        this.toast.show('Debes cambiar tu contraseña', 'warning', 5000);
        await this.router.navigateByUrl('/profile');
      } else {
        await this.router.navigateByUrl('/');
      }
    } catch (err: any) {
      const message = err?.error?.error || err?.error?.message || err?.message || 'Error al iniciar sesión';
      this.toast.show(message, 'error', 5000);
      this.error.set(null);
    } finally {
      this.loading.set(false);
    }
  }
}
