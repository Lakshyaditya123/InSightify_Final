import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-landing',
  standalone: true,
  imports: [],
  templateUrl: './landing.html',
  styleUrl: './landing.css'
})


export class Landing {

   ideaBoxes = [
  { size: 'large', title: 'AI Brainstorm', content: 'Explore ideas with AI' },
  { size: 'small', title: 'Quick Tip', content: 'Fast insights' },
  { size: 'medium', title: 'Featured', content: 'Highlighted thoughts' },
  { size: 'small', title: 'Buzzing Idea', content: 'Trending concept' },
  { size: 'large', title: 'Innovation', content: 'Breakthrough zone' },
  { size: 'small', title: 'Snippets', content: 'Short notes' },
  { size: 'medium', title: 'Recommended', content: 'AI picks' },
  { size: 'small', title: 'Drafts', content: 'Unpolished but brilliant' },
  { size: 'medium', title: 'Saved', content: 'Your favs' }
];

   shuffledBoxes = this.shuffleArray([...this.ideaBoxes]);
firstRow = [...this.shuffleArray(this.ideaBoxes), ...this.shuffleArray(this.ideaBoxes)];
secondRow = [...this.shuffleArray(this.ideaBoxes), ...this.shuffleArray(this.ideaBoxes)];
// For infinite scroll effect, do NOT keep adding to the array. Use CSS animation instead.


shuffleArray(array: any[]) {
  return array.sort(() => Math.random() - 0.5);
}

  constructor(private router: Router) {}


   goToLogin() {
    this.router.navigate(['/login']);}

}