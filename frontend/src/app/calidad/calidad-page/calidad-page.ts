import { Component } from '@angular/core';
import { LayoutService } from '../../core/services/layout-service';

@Component({
  selector: 'app-calidad-page',
  imports: [],
  templateUrl: './calidad-page.html',
  styleUrl: './calidad-page.css',
})
export class CalidadPage {
  constructor(private titleService: LayoutService) {
    this.titleService.title.set('Calidad');
  }
}
