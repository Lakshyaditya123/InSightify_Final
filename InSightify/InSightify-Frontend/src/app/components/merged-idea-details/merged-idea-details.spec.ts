import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MergedIdeaDetails } from './merged-idea-details';

describe('MergedIdeaDetails', () => {
  let component: MergedIdeaDetails;
  let fixture: ComponentFixture<MergedIdeaDetails>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MergedIdeaDetails]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MergedIdeaDetails);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
