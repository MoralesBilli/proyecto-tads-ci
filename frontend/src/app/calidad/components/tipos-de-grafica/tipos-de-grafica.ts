import { Component, input, model, output } from '@angular/core';

@Component({
  selector: 'app-tipos-de-grafica',
  imports: [],
  templateUrl: './tipos-de-grafica.html',
  styleUrl: './tipos-de-grafica.css',
})
export class TiposDeGrafica {
  public readonly graficaSeleccionada = model('')

  protected getTailwindBgColors(grafica: string) {
    if (this.graficaSeleccionada() === grafica) return 'bg-primary/10 hover:bg-primary/25 border-primary text-primary'
    return 'bg-base-content/10 hover:bg-base-content/25 border-base-content text-base-content'
  }

  handleGraficaSeleccionadaChange(nuevaGrafica: string) {
    this.graficaSeleccionada.set(nuevaGrafica)
  }
}
