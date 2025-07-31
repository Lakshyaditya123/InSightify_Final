import { Component, OnInit, HostListener, ElementRef, Output, EventEmitter, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth';
import { UserProfile } from '../user-profile/user-profile';
import { FormsModule } from '@angular/forms';
import { Idea_small, Merged_idea_small } from '../../services/api-interfaces';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, UserProfile, FormsModule],
  templateUrl: './navbar.html',
  styleUrls: ['./navbar.css']
})
export class Navbar implements OnInit {
  // Inputs from parent to get data for suggestions
  @Input() allIdeas: Idea_small[] = [];
  @Input() allMergedIdeas: Merged_idea_small[] = [];
  @Output() ideaSearch = new EventEmitter<string>();

  isDropdownOpen = false;
  isProfilePanelOpen = false;
  idea_search_input = '';
  suggestions: string[] = [];
  isSuggestionsVisible = false;

  constructor(
    private authService: AuthService,
    private router: Router,
    private elementRef: ElementRef
  ) {}

  ngOnInit() {}

  @HostListener('document:click', ['$event'])
  onDocumentClick(event: Event) {
    if (!this.elementRef.nativeElement.querySelector('.profile-section').contains(event.target)) {
      this.isDropdownOpen = false;
    }
    if (!this.elementRef.nativeElement.querySelector('.search-container').contains(event.target)) {
      this.isSuggestionsVisible = false;
    }
  }

  onSearchInput() {
    const query = this.idea_search_input.toLowerCase().trim();
    if (query.length < 5) {
      this.suggestions = [];
      this.isSuggestionsVisible = false;
      if (query.length === 0) {
        this.ideaSearch.emit('');
      }
      return;
    }

    const allSuggestions = new Set<string>();
    this.allIdeas.forEach(card => {
      if (card.idea_details.title.toLowerCase().includes(query)) allSuggestions.add(card.idea_details.title);
      if (card.idea_details.subject.toLowerCase().includes(query)) allSuggestions.add(card.idea_details.subject);
      if (card.user_details.name.toLowerCase().includes(query)) allSuggestions.add(card.user_details.name);
    });

    this.allMergedIdeas.forEach(card => {
      if (card.merged_idea_details.title.toLowerCase().includes(query)) allSuggestions.add(card.merged_idea_details.title);
      if (card.merged_idea_details.subject.toLowerCase().includes(query)) allSuggestions.add(card.merged_idea_details.subject);
      card.user_idea_details.forEach(user => {
        if (user.user_details.name.toLowerCase().includes(query)) allSuggestions.add(user.user_details.name);
      });
    });

    this.suggestions = Array.from(allSuggestions).slice(0, 5); // Show top 5 suggestions
    this.isSuggestionsVisible = this.suggestions.length > 0;
  }

  /**
   * Finalizes the search and filters the wall.
   */
  onSearchSubmit() {
    this.ideaSearch.emit(this.idea_search_input);
    this.isSuggestionsVisible = false; // Hide suggestions after search
  }

  /**
   * Sets the input value and triggers a search when a suggestion is clicked.
   */
  selectSuggestion(suggestion: string) {
    this.idea_search_input = suggestion;
    this.onSearchSubmit();
  }

  toggleDropdown(event: Event) {
    event.stopPropagation();
    this.isDropdownOpen = !this.isDropdownOpen;
  }

  openProfilePanel() {
    this.isProfilePanelOpen = true;
    this.isDropdownOpen = false;
  }

  closeProfilePanel() {
    this.isProfilePanelOpen = false;
  }

  refreshPage() {
    window.location.reload();
  }

  logout() {
    this.authService.clearUser();
    this.router.navigate(['/login']);
    this.isDropdownOpen = false;
  }
}
