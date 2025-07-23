import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './navbar.html',
  styleUrl: './navbar.css'
})
export class Navbar {
  constructor(private router: Router, private auth : AuthService) {

  }

  // tags = ['AI', 'UI/UX', 'Backend', 'ML', 'Research'];
  // selectedTags: string[] = [];
  // toggleTag(tag: string) {
  //   const index = this.selectedTags.indexOf(tag);
  //   if (index > -1) {
  //     this.selectedTags.splice(index, 1); // Remove
  //   } else {
  //     this.selectedTags.push(tag); // Add
  //   }
  // }

  // isTagSelected(tag: string): boolean {
  //   return this.selectedTags.includes(tag);
  // }

  navigateToProfile() {
    this.router.navigate(['/profile']);
  }
  navigateToHome() {
    this.auth.clearUser()
    this.router.navigate(['/login']);
  }
}
