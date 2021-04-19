import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BoxDisplayComponent } from './box-display.component';

describe('BoxesDisplayComponent', () => {
  let component: BoxDisplayComponent;
  let fixture: ComponentFixture<BoxDisplayComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BoxDisplayComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BoxDisplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
