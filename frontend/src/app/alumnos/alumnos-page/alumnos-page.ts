import { Component, inject } from '@angular/core';
import { LayoutService } from '../../core/services/layout-service';
import { AlumnosList } from '../components/alumnos-list/alumnos-list';
import { AlumnoDetalle } from '../components/alumno-detalle/alumno-detalle';
import { AlumnosService } from '../services/alumnos-service';
import { Alumno } from '../models/alumnoSchema';
import { AlumnosFab } from '../components/alumnos-fab/alumnos-fab';

@Component({
  selector: 'app-alumnos-page',
  imports: [AlumnosList, AlumnoDetalle, AlumnosFab],
  templateUrl: './alumnos-page.html',
  styleUrl: './alumnos-page.css',
})
export class AlumnosPage {
  private readonly layoutService = inject(LayoutService);
  private readonly alumnosService = inject(AlumnosService);

  protected readonly alumnos = this.alumnosService.alumnos;
  protected readonly alumnoSeleccionado = this.alumnosService.alumnoSeleccionado;
  protected readonly alumnoDetalle = this.alumnosService.alumnoSeleccionadoDetalle;

  protected handleAlumnoSeleccionadoChange(alumno: Alumno) {
    this.alumnosService.alumnoSeleccionado.set(alumno);
  }

  constructor() {
    this.layoutService.title.set('Alumnos');
  }
}
