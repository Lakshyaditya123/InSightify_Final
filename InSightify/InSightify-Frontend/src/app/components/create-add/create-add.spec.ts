import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateAdd } from './create-add';

describe('CreateAdd', () => {
  let component: CreateAdd;
  let fixture: ComponentFixture<CreateAdd>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateAdd]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CreateAdd);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
