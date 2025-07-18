import {Component, Input} from '@angular/core';
import {CommonModule} from '@angular/common';
import { Idea_large } from '../../services/api-interfaces';

@Component({
  selector: 'app-idea-details',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './idea-details.html',
  styleUrl: './idea-details.css'
})
export class IdeaDetails {
  @Input() cardData!: Idea_large;

  // Convert size to idea type label
  getIdeaTypeLabel(): string {
    return 'Human Idea';
  }

  // Get CSS class for idea type badge
  getIdeaTypeClass(): string {
    return 'bg-primary'; // Human ideas - blue
  }
}
