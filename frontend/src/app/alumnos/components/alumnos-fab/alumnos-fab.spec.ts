import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AlumnosFab } from './alumnos-fab';

describe('AlumnosFab', () => {
  let component: AlumnosFab;
  let fixture: ComponentFixture<AlumnosFab>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AlumnosFab]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AlumnosFab);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
