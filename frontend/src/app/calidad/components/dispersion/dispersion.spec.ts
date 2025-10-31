import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Dispersion } from './dispersion';

describe('Dispersion', () => {
  let component: Dispersion;
  let fixture: ComponentFixture<Dispersion>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Dispersion]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Dispersion);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
