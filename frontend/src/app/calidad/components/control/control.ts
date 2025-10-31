import { Component, computed, input } from '@angular/core';
import { ChartData } from 'chart.js';
import { BaseChartDirective } from 'ng2-charts';

const log = (something: unknown) => {
  console.log(something)
  return log
}

@Component({
  selector: 'app-control',
  imports: [BaseChartDirective],
  templateUrl: './control.html',
  styleUrl: './control.css',
})
export class Control<T> {
  readonly data = input.required<T[]>()
  readonly getX = input.required<(item: T) => number>()
  readonly getY = input.required<(item: T) => number>()

  protected readonly avg = computed(() => this.data().reduce(
    (acum, curr) => acum + this.getY()(curr), 0
  ) / this.data().length)

  protected stdDev = computed(() => Math.sqrt(
    this.data()
    .map(item => Math.pow(this.getY()(item) - this.avg(), 2))
    .reduce((acum, curr) => acum + curr, 0) / (this.data().length - 1)
  ))

  protected readonly chartData = computed<ChartData<'line'>>(() => ({
    labels: this.data().map(item => this.getX()(item)),
    datasets: [
      {
        data: this.data().map(item => this.getY()(item)),
        label: 'Calificación x Unidad',
        type: 'line',
      },
      {
        data: Array.from({ length: this.data().length }).fill(this.avg()) as number[],
        label: 'Limite de Control Central',
        type: 'line',
        pointRadius: 0,
        borderDash: [6, 4]
      },
      {
        data: Array.from({ length: this.data().length }).fill(this.avg() + 1 * this.stdDev()) as number[],
        label: 'Limite de Control Superior',
        type: 'line',
        pointRadius: 0,
        borderDash: [6, 4]
      },
      {
        data:  Array.from({ length: this.data().length }).fill(this.avg() - 1 * this.stdDev()) as number[],
        label: 'Limite de Control Inferior',
        type: 'line',
        pointRadius: 0,
        borderDash: [6, 4]
      }
    ]
  }))
}
