import { computed, Injectable, signal } from '@angular/core';
import { Alumno } from '../models/alumnoSchema';
import { AlumnoDetalle, alumnoDetalleSchema } from '../models/alumnoDetalleSchema';

@Injectable({
  providedIn: 'root'
})
export class AlumnosService {
  readonly alumnos = signal<Alumno[]>([
    {
      "numeroDeControl": "21214530",
      "nombre": "Sharona",
      "apellidoPaterno": "Welbelove",
      "apellidoMaterno": "Gunning",
      "factoresDeRiesgo": [

      ]
    },
    {
      "numeroDeControl": "21219531",
      "nombre": "Jeannette",
      "apellidoPaterno": "Pargetter",
      "apellidoMaterno": "Bathurst",
      "factoresDeRiesgo": [
        "Economico",
        "Contextual"
      ]
    },
    {
      "numeroDeControl": "21216371",
      "nombre": "Tamarra",
      "apellidoPaterno": "Llewelly",
      "apellidoMaterno": "Gude",
      "factoresDeRiesgo": [

      ]
    },
    {
      "numeroDeControl": "21216705",
      "nombre": "Shaine",
      "apellidoPaterno": "Reskelly",
      "apellidoMaterno": "Elward",
      "factoresDeRiesgo": [
        "Economico",
        "Institucional",
        "Academico"
      ]
    },
    {
      "numeroDeControl": "21217241",
      "nombre": "Else",
      "apellidoPaterno": "Fane",
      "apellidoMaterno": "Treagus",
      "factoresDeRiesgo": [
        "Contextual",
        "Economico",
        "Academico",
        "Psicosocial",
        "Institucional"
      ]
    },
    {
      "numeroDeControl": "21219085",
      "nombre": "Freddie",
      "apellidoPaterno": "McNeice",
      "apellidoMaterno": "Chamberlain",
      "factoresDeRiesgo": [
        "Economico",
        "Institucional",
        "Contextual"
      ]
    },
    {
      "numeroDeControl": "21216873",
      "nombre": "Anthe",
      "apellidoPaterno": "Gobeau",
      "apellidoMaterno": "Chatelet",
      "factoresDeRiesgo": [
        "Psicosocial",
        "Economico",
        "Contextual",
        "Institucional"
      ]
    },
    {
      "numeroDeControl": "21214415",
      "nombre": "Dot",
      "apellidoPaterno": "Lindell",
      "apellidoMaterno": null,
      "factoresDeRiesgo": [
        "Contextual",
        "Economico"
      ]
    },
    {
      "numeroDeControl": "21215637",
      "nombre": "Fianna",
      "apellidoPaterno": "Thowes",
      "apellidoMaterno": null,
      "factoresDeRiesgo": [

      ]
    },
    {
      "numeroDeControl": "21219628",
      "nombre": "Jaymee",
      "apellidoPaterno": "Hurrell",
      "apellidoMaterno": null,
      "factoresDeRiesgo": [
        "Academico"
      ]
    }
  ]);

  readonly alumnoSeleccionado = signal<Alumno|null>(null);
  readonly alumnoSeleccionadoDetalle = computed<AlumnoDetalle | null>(() => {
    const alumno = this.alumnoSeleccionado();
    if (!alumno) return null;

    const detalle = {
      numeroDeControl: alumno.numeroDeControl,
      nombre: alumno.nombre,
      apellidoPaterno: alumno.apellidoPaterno,
      apellidoMaterno: alumno.apellidoMaterno,
      genero: 'HOMBRE',
      estado: 'VIGENTE',
      semestre: 8,
      nombreCarrera: 'Ing. En Sistemas Computacionales',
      modalidadCarrera: 'Presencial',
      factoresDeRiesgo: alumno.factoresDeRiesgo,
      inscripciones: [
        {
          grupo: 'SC8A',
          nombreMateria: 'Programacion Web',
          serieMateria: 'XXX-0001',
          calificaciones: [
            { unidad: 1, calificacion: 90, faltas: 0 },
            { unidad: 2, calificacion: 80, faltas: 1 }
          ]
        },
        {
          grupo: 'SC9B',
          nombreMateria: 'Temas Avanzados de Desarrollo de Software',
          serieMateria: 'XXX-0002',
          calificaciones: [
            { unidad: 1, calificacion: 100, faltas: 0 }
          ]
        }
      ],
      fotoUrl: `https://i.pravatar.cc/200?u=${alumno.numeroDeControl}`
    };

    const parsed = alumnoDetalleSchema.safeParse(detalle);
    return parsed.success ? parsed.data : null;
  });
}
