import { Component, OnInit, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { firstValueFrom } from 'rxjs';

// Import child components and services
import { Navbar } from '../../components/navbar/navbar';
import { IdeaDetails } from '../../components/idea-details/idea-details';
import { MergedIdeaDetails } from '../../components/merged-idea-details/merged-idea-details';
import { AuthService } from '../../services/auth';
import { IdeaService } from '../../services/idea';
import { ApiResponse, CurrUser, Idea_large, Merged_idea_large } from '../../services/api-interfaces';

// Declare bootstrap for modal control
declare var bootstrap: any;

@Component({
  selector: 'app-admin-screen',
  templateUrl: './admin-screen.html',
  styleUrls: ['./admin-screen.css'],
  standalone: true,
  imports: [CommonModule, Navbar, IdeaDetails, MergedIdeaDetails],
})
export class AdminScreen implements OnInit, AfterViewInit {
  // --- STATE ---
  admin = {
    name: 'Admin User',
    email: 'adminname1235@gmail.com',
    phone: '+91 1254567890',
    role: 'admin',
  };

  // Updated mock data with IDs and types
  submissions = [
    { id: 1, name: 'AI-Powered Personal Finance Advisor', desc: 'An app that uses machine learning to provide personalized financial advice.', isMerged: false },
    { id: 2, name: 'Eco-Friendly Packaging Solution', desc: 'Developing biodegradable packaging from seaweed.', isMerged: false },
    { id: 1, name: 'Virtual Reality Language Learning', desc: 'Immersive language learning through VR scenarios.', isMerged: true },
    { id: 4, name: 'Automated Home Hydroponics System', desc: 'A smart system for growing herbs and vegetables indoors.', isMerged: false },
  ];
  
  // State for managing the modal
  selectedCard: Idea_large | null = null;
  selectedMergedCard: Merged_idea_large | null = null;
  isCommentsVisible = false;
  modalType: 'idea' | 'merged-idea' | null = null;
  ideaModal: any;
  currentUserId: number = -1;

  constructor(
    private router: Router, 
    private authService: AuthService,
    private ideaService: IdeaService // Injected IdeaService
  ) {}

  ngOnInit() {
    const currentUser = this.authService.getCurrentUser();
    if (currentUser) {
      this.currentUserId = currentUser.user_id;
    } else {
      console.error("Admin/User not logged in, redirecting.");
      this.router.navigate(['/']);
    }
  }

  ngAfterViewInit() {
    const modalElement = document.getElementById('admin_idea_details_modal');
    if (modalElement) {
      this.ideaModal = new bootstrap.Modal(modalElement);
      // Ensure state is reset whenever the modal is closed
      modalElement.addEventListener('hidden.bs.modal', () => {
        this.resetModalState();
      });
    }
  }

  /**
   * Opens the idea details modal after fetching the relevant data.
   * @param submission The submission object that was clicked.
   */
  async openSubmissionModal(submission: any) {
    this.resetModalState();

    try {
      let result: ApiResponse;
      if (submission.isMerged) {
        this.modalType = 'merged-idea';
        result = await firstValueFrom(this.ideaService.get_idea(null, submission.id, this.currentUserId));
        if (result.errCode === 0) this.selectedMergedCard = result.datarec;
      } else {
        this.modalType = 'idea';
        result = await firstValueFrom(this.ideaService.get_idea(submission.id, null, this.currentUserId));
        if (result.errCode === 0) this.selectedCard = result.datarec;
      }

      if (result?.errCode === 0) {
        this.ideaModal.show();
      } else {
        console.error('Failed to get submission details:', result?.message);
        alert('Could not load idea details.');
      }
    } catch (error) {
      console.error('Error opening submission modal:', error);
      alert('An error occurred while loading idea details.');
    }
  }

  /**
   * Closes the currently active idea modal.
   */
  closeIdeaModal() {
    if (this.ideaModal) {
      this.ideaModal.hide();
    }
  }

  /**
   * Resets all modal-related state variables to their initial values.
   */
  private resetModalState() {
    this.selectedCard = null;
    this.selectedMergedCard = null;
    this.isCommentsVisible = false;
    this.modalType = null;
  }

  toggleCommentsVisibility() {
    this.isCommentsVisible = !this.isCommentsVisible;
  }

  /**
   * Handles the 'Approve' action. Stops the click from opening the modal.
   */
  onApprove(idea: any, event: MouseEvent) {
    event.stopPropagation();
    alert('Approved: ' + idea.name);
  }

  /**
   * Handles the 'Decline' action. Stops the click from opening the modal.
   */
  onDecline(idea: any, event: MouseEvent) {
    event.stopPropagation();
    alert('Declined: ' + idea.name);
  }

  onSwitchToUser() {
    this.router.navigate(['/homescreen']);
  }
}
