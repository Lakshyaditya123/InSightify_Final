import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AdminScreen } from './admin-screen';

describe('AdminScreen', () => {
  let component: AdminScreen;
  let fixture: ComponentFixture<AdminScreen>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AdminScreen]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AdminScreen);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
