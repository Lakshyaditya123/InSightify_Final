import {Component, Input} from '@angular/core';
import {CommonModule} from '@angular/common';

@Component({
  selector: 'app-idea-details',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './idea-details.html',
  styleUrl: './idea-details.css'
})
export class IdeaDetails {
  @Input() cardData: any;
}
