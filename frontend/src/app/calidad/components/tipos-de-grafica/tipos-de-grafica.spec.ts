import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TiposDeGrafica } from './tipos-de-grafica';

describe('TiposDeGrafica', () => {
  let component: TiposDeGrafica;
  let fixture: ComponentFixture<TiposDeGrafica>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TiposDeGrafica]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TiposDeGrafica);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
