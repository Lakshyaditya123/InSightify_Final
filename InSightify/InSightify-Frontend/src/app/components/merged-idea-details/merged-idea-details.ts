import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Merged_idea_large } from '../../services/api-interfaces';

@Component({
  selector: 'app-merged-idea-details',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './merged-idea-details.html',
  styleUrl: './merged-idea-details.css'  // Reusing your existing styles
})
export class MergedIdeaDetails {
  @Input() cardData!: Merged_idea_large;
}