import { Component, computed, input } from '@angular/core';
import { BaseChartDirective } from 'ng2-charts';

@Component({
  selector: 'app-dispersion',
  imports: [BaseChartDirective],
  templateUrl: './dispersion.html',
  styleUrl: './dispersion.css',
})
export class Dispersion<T> {
  readonly data = input.required<T[]>()
  readonly getX = input.required<(item: T) => number>()
  readonly getY = input.required<(item: T) => number>()

  protected readonly chartData = computed(() => ({
    datasets: [
      {
        data: this.data().map(item => ({
          x: this.getX()(item),
          y: this.getY()(item)
        })),
        label: 'Faltas vs Calificación',
        type: 'scatter'
      }
    ]
  }))
}
