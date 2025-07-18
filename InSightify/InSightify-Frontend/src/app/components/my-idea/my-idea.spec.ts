import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MyIdea } from './my-idea';

describe('MyIdea', () => {
  let component: MyIdea;
  let fixture: ComponentFixture<MyIdea>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MyIdea]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MyIdea);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
