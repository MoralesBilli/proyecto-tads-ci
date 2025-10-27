import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: 'alumnos', pathMatch: 'full' },
  {
    path: 'alumnos',
    loadComponent: () => import("./alumnos/alumnos-page/alumnos-page").then(c => c.AlumnosPage),
    title: 'Alumnos'
  },
  {
    path: 'calidad',
    loadComponent: () => import("./calidad/calidad-page/calidad-page").then(c => c.CalidadPage),
    title: 'Calidad'
  }
];
