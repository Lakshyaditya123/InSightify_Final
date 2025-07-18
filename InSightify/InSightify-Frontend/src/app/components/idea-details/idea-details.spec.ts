import { ComponentFixture, TestBed } from '@angular/core/testing';

import { IdeaDetails } from './idea-details';

describe('IdeaDetails', () => {
  let component: IdeaDetails;
  let fixture: ComponentFixture<IdeaDetails>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [IdeaDetails]
    })
    .compileComponents();

    fixture = TestBed.createComponent(IdeaDetails);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
