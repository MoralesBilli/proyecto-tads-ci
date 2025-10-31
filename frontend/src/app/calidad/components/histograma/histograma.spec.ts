import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Histograma } from './histograma';

describe('Histograma', () => {
  let component: Histograma;
  let fixture: ComponentFixture<Histograma>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Histograma]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Histograma);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
