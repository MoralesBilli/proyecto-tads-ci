import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AlumnosList } from './alumnos-list';

describe('AlumnosList', () => {
  let component: AlumnosList;
  let fixture: ComponentFixture<AlumnosList>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AlumnosList]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AlumnosList);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
