import { Component, OnInit, HostListener, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth';
import { UserProfile } from '../user-profile/user-profile';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, UserProfile],
  templateUrl: './navbar.html',
  styleUrls: ['./navbar.css']
})
export class Navbar implements OnInit {
  isDropdownOpen = false;
  isProfilePanelOpen = false;

  constructor(
    private authService: AuthService,
    private router: Router,
    private elementRef: ElementRef
  ) {}

  ngOnInit() {}

  @HostListener('document:click', ['$event'])
  onDocumentClick(event: Event) {
    // This will now correctly close the dropdown only when clicking OUTSIDE the profile section.
    if (!this.elementRef.nativeElement.querySelector('.profile-section').contains(event.target)) {
      this.isDropdownOpen = false;
    }
  }

  toggleDropdown(event: Event) {
    event.stopPropagation(); // Prevents the document click listener from firing immediately.
    this.isDropdownOpen = !this.isDropdownOpen;
  }

  openProfilePanel() {
    this.isProfilePanelOpen = true;
    this.isDropdownOpen = false; // This line ensures the dropdown closes.
  }

  closeProfilePanel() {
    this.isProfilePanelOpen = false;
  }

  logout() {
    this.authService.clearUser();
    this.router.navigate(['/login']);
    this.isDropdownOpen = false;
  }

  navigateToHome() {
    // this.router.navigate(['/homescreen']);
  }
}
