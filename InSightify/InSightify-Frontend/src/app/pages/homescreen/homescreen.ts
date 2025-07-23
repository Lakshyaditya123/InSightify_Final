import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { firstValueFrom } from 'rxjs';
import { Navbar } from '../../components/navbar/navbar';
import { IdeaDetails } from '../../components/idea-details/idea-details';
import { MergedIdeaDetails } from '../../components/merged-idea-details/merged-idea-details';
import { CreateAdd } from '../../components/create-add/create-add';
import { Comments } from '../../components/comments/comments';
import { IdeaService } from '../../services/idea';
import { ApiResponse, Idea_small, Idea_large, Merged_idea_small, My_idea, Merged_idea_large, CurrUser} from '../../services/api-interfaces';
import { AuthService } from '../../services/auth';
import { Router } from '@angular/router';
import { VotesSection } from '../../components/votes-section/votes-section';


declare var bootstrap: any;

@Component({
  selector: 'app-homescreen',
  standalone: true,
  imports: [CommonModule, Navbar, IdeaDetails, CreateAdd, MergedIdeaDetails, VotesSection],
  templateUrl: './homescreen.html',
  styleUrl: './homescreen.css'
})
export class Homescreen implements OnInit {
  selectedCard: Idea_large | null = null;
  selectedMergedCard: Merged_idea_large | null = null;
  selectedCommentCard: Comment | null = null;
  all_cards: Idea_small[] = [];
  all_merged_cards: Merged_idea_small[] = [];
  all_my_cards: My_idea[] = [];
  currentUserId: number = -1;
  mySpace=false;

  constructor(private ideaService: IdeaService, private authService: AuthService, private router: Router) {}

  ngOnInit() {
    const currentUser: CurrUser | null = this.authService.getCurrentUser();
    if (currentUser) {
      this.currentUserId = currentUser.user_id;
      this.get_all_ideas();
    } else {
      this.router.navigate(['/']);
      console.error('User not logged in!');
    }
  }

  get_all_ideas() {
    this.ideaService.get_all_main_walls(this.currentUserId).subscribe((res: ApiResponse) => {
      if (res.errCode === 0 && res.datarec?.all_ideas) {
        this.all_cards = res.datarec.all_ideas;
        this.all_merged_cards = res.datarec.all_merged_ideas;
        this.all_my_cards = res.datarec.all_my_ideas;
        console.log("all_merged_ideas", this.all_merged_cards);
        console.log("all_my_ideas", this.all_my_cards);
      } else {
        console.error("Failed to load ideas:", res.message);
      }
    });
  }

getStatusColor(status: number): string {
  switch (status) {
    case -1: return 'red';
    case 0: return 'gray';
    case 1: return 'green';
    default: return 'gray'; // fallback
  }
}
async open_my_space_idea_modal(card: My_idea) {
  this.mySpace = true;
  try {
    
    const result: ApiResponse = await firstValueFrom(
      this.ideaService.get_idea(card.idea_id, null, this.currentUserId)
    );

    if (result.errCode === 0 && result.datarec) {
      this.selectedCard = result.datarec;
    } else {
      console.error("Failed to get idea:", result.message);
    }

    const modalElement = document.getElementById('ticket_details_modal');
    if (modalElement) new bootstrap.Modal(modalElement).show();

  } catch (error: any) {
    console.error('Error fetching idea details:', error);
  }
}


async open_ticket_details_modal(card: Idea_small ) {
  try {
    this.mySpace = false;
    const result: ApiResponse = await firstValueFrom(
      this.ideaService.get_idea(card.idea_details.id, null, this.currentUserId)
    );

    if (result.errCode === 0 && result.datarec) {
      this.selectedCard = result.datarec;
    } else {
      console.error("Failed to get idea:", result.message);
    }

    const modalElement = document.getElementById('ticket_details_modal');
    if (modalElement) new bootstrap.Modal(modalElement).show();
  } catch (error: any) {
    console.error('Error fetching idea details:', error);
  }
}


async open_merged_ticket_details_modal(card: Merged_idea_small) {
  try {
    const result: ApiResponse = await firstValueFrom(
      this.ideaService.get_idea(null, card.merged_idea_details.id, this.currentUserId)
    );

    if (result.errCode === 0 && result.datarec) {
      this.selectedMergedCard = result.datarec; // Full Merged_idea_large
    } else {
      console.error("Failed to fetch merged idea details:", result.message);
    }

    const modalElement = document.getElementById('merged_ticket_details_modal');
    if (modalElement) new bootstrap.Modal(modalElement).show();

  } catch (error) {
    console.error("Error loading merged idea details:", error);
  }
}

  close_ticket_details_modal() {
    // Move focus before hiding modal
    const mainBtn = document.querySelector('.add-more-btn') as HTMLElement;
    if (mainBtn) mainBtn.focus();
    else document.body.focus();
    const modalElement = document.getElementById('ticket_details_modal');
    if (modalElement) {
      const modal = bootstrap.Modal.getInstance(modalElement);
      if (modal) modal.hide();
    }
    this.selectedCard = null;
  }

  close_merged_ticket_details_modal() {
    // Move focus before hiding modal
    const mainBtn = document.querySelector('.add-more-btn') as HTMLElement;
    if (mainBtn) mainBtn.focus();
    else document.body.focus();
    const modalElement = document.getElementById('merged_ticket_details_modal');
    if (modalElement) {
      const modal = bootstrap.Modal.getInstance(modalElement);
      if (modal) modal.hide();
    }
    this.selectedMergedCard = null;
  }

  open_add_idea_modal() {
    const modalElement = document.getElementById('addIdea_modal');
    if (modalElement) new bootstrap.Modal(modalElement).show();
  }

  close_add_idea_modal() {
    // Move focus before hiding modal
    const mainBtn = document.querySelector('.add-more-btn') as HTMLElement;
    if (mainBtn) mainBtn.focus();
    else document.body.focus();
    const modalElement = document.getElementById('addIdea_modal');
    if (modalElement) {
      const modal = bootstrap.Modal.getInstance(modalElement);
      if (modal) modal.hide();
    }
  }
}