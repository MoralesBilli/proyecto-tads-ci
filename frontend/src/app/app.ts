import { Component, inject, signal } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { LayoutService } from './core/services/layout-service';
import { ToastContainer } from './core/components/toast-container/toast-container';

interface Link {
  readonly label: string;
  readonly link: string;
}

@Component({
  selector: 'app-root',
  imports: [RouterLink, RouterLinkActive, RouterOutlet, ToastContainer],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly layoutService = inject(LayoutService);
  protected readonly bottomNavigation = signal<Link[]>([
    { label: 'Alumnos', link: '/alumnos' },
    { label: 'Calidad', link: '/calidad' }
  ]);
}
