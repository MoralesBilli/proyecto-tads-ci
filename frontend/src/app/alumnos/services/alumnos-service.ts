import { inject, Injectable, signal } from '@angular/core';
import { Alumno, alumnoSchema } from '../models/alumnoSchema';
import { alumnoDetalleSchema } from '../models/alumnoDetalleSchema';
import { HttpClient, httpResource } from '@angular/common/http';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AlumnosService {
  private readonly apiUrl = environment.apiUrl
  private readonly http = inject(HttpClient)

  readonly alumnos = httpResource(
    () => `${this.apiUrl}/alumnos`,
    {
      parse: data => alumnoSchema.array().parse(data),
    }
  )

  readonly alumnoSeleccionado = signal<Alumno|null>(null);
  readonly alumnoSeleccionadoDetalle = httpResource(
    () => {
      const numeroDeControl = this.alumnoSeleccionado()?.numeroDeControl;
      if (!numeroDeControl) return

      return `${this.apiUrl}/alumno_detalle/${numeroDeControl}`
    },
    {
      parse: data => alumnoDetalleSchema.parse(data),
    }
  )

  importarAlumnos(archivo: File) {
    const formData = new FormData();
    formData.append('archivo', archivo, archivo.name);

    return this.http.post(
      `${this.apiUrl}/importar/grupos`,
      formData
    )
  }

  importarCalificaciones(archivo: File) {
    const formData = new FormData();
    formData.append('archivo', archivo, archivo.name);

    return this.http.post(
      `${this.apiUrl}/importar/calificaciones`,
      formData
    )
  }
}
