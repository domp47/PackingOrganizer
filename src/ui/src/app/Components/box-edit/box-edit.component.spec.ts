import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BoxEditComponent } from './box-edit.component';

describe('BoxEditComponent', () => {
  let component: BoxEditComponent;
  let fixture: ComponentFixture<BoxEditComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [BoxEditComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BoxEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
