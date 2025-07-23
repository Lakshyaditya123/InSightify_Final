import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VotesSection } from './votes-section';

describe('VotesSection', () => {
  let component: VotesSection;
  let fixture: ComponentFixture<VotesSection>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [VotesSection]
    })
    .compileComponents();

    fixture = TestBed.createComponent(VotesSection);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
