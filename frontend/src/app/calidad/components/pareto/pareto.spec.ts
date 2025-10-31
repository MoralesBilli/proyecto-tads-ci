import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Pareto } from './pareto';

describe('Pareto', () => {
  let component: Pareto;
  let fixture: ComponentFixture<Pareto>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Pareto]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Pareto);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
