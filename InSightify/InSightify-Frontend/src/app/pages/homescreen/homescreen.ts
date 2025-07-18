import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { firstValueFrom } from 'rxjs';
import { Navbar } from '../../components/navbar/navbar';
import { IdeaDetails } from '../../components/idea-details/idea-details';
import { MergedIdeaDetails } from '../../components/merged-idea-details/merged-idea-details';
import { CreateAdd } from '../../components/create-add/create-add';
import { Comments } from '../../components/comments/comments';
import { IdeaService } from '../../services/idea';
import { ApiResponse, Idea_small, Idea_large, Merged_idea_small, My_idea,Merged_idea_large } from '../../services/api-interfaces';
import { AuthService } from '../../services/auth';
import { CurrUser } from '../../services/api-interfaces';

declare var bootstrap: any;

@Component({
  selector: 'app-homescreen',
  standalone: true,
  imports: [CommonModule, Navbar, IdeaDetails, CreateAdd, MergedIdeaDetails],
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

  constructor(private ideaService: IdeaService, private authService: AuthService) {}

  ngOnInit() {
    const currentUser: CurrUser | null = this.authService.getCurrentUser();
    if (currentUser) {
      this.currentUserId = currentUser.user_id;
      this.get_all_ideas();
    } else {
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

  isMergedIdea(idea: any): idea is Merged_idea_small {
    return 'merged_idea_details' in idea;
  }

  async upvoteIdea(idea: Idea_small | Merged_idea_small) {
    const id = this.isMergedIdea(idea) ? idea.merged_idea_details.id : idea.idea_details.id;
    const vote_type = 1;

    if (idea.vote_details.user_vote_details?.vote_type === vote_type) {
      await this.removeVote(idea);
    } else {
      try {
        const payload = this.isMergedIdea(idea)
          ? { merged_idea_id: id, user_id: this.currentUserId, vote_type }
          : { idea_id: id, user_id: this.currentUserId, vote_type };

        const result: ApiResponse = await firstValueFrom(this.ideaService.upvoteIdea(payload));
        if (result.errCode === 0 && result.datarec?.vote_details) {
          idea.vote_details = result.datarec.vote_details;
        } else {
          console.error("Failed to upvote:", result.message);
        }
      } catch (error) {
        console.error('Error upvoting idea:', error);
      }
    }
  }


  async downvoteIdea(idea: Idea_small | Merged_idea_small) {
    const id = this.isMergedIdea(idea) ? idea.merged_idea_details.id : idea.idea_details.id;
    const vote_type = -1;

    if (idea.vote_details.user_vote_details?.vote_type === vote_type) {
      await this.removeVote(idea);
    } else {
      try {
        const payload = this.isMergedIdea(idea)
          ? { merged_idea_id: id, user_id: this.currentUserId, vote_type }
          : { idea_id: id, user_id: this.currentUserId, vote_type };

        const result: ApiResponse = await firstValueFrom(this.ideaService.downvoteIdea(payload));
        if (result.errCode === 0 && result.datarec?.vote_details) {
          idea.vote_details = result.datarec.vote_details;
        } else {
          console.error("Failed to downvote:", result.message);
        }
      } catch (error) {
        console.error('Error downvoting idea:', error);
      }
    }
  }

  async removeVote(idea: Idea_small | Merged_idea_small) {
    const id = this.isMergedIdea(idea) ? idea.merged_idea_details.id : idea.idea_details.id;
    try {
      const payload = this.isMergedIdea(idea)
        ? { merged_idea_id: id, user_id: this.currentUserId, vote_type: 0 }
        : { idea_id: id, user_id: this.currentUserId, vote_type: 0 };

      const result: ApiResponse = await firstValueFrom(this.ideaService.removeVote(payload));
      if (result.errCode === 0 && result.datarec?.vote_details) {
        idea.vote_details = result.datarec.vote_details;
      } else {
        console.error("Failed to remove vote:", result.message);
      }
    } catch (error) {
      console.error('Error removing vote:', error);
    }
  }

  getVoteDisplay(totalVotes: number): string {
    return totalVotes >= 1000 ? (totalVotes / 1000).toFixed(1) + 'k' : totalVotes.toString();
  }

  getVoteColorClass(totalVotes: number): string {
    return totalVotes > 0 ? 'text-success' : totalVotes < 0 ? 'text-danger' : 'text-muted';
  }

  getTotalVotes(idea: Idea_small | Merged_idea_small): number {
    return idea.vote_details.idea_vote_details.total;
  }

  getUpvotes(idea: Idea_small | Merged_idea_small): number {
    return idea.vote_details.idea_vote_details.upvotes;
  }

  getDownvotes(idea: Idea_small | Merged_idea_small): number {
    return idea.vote_details.idea_vote_details.downvotes;
  }

  getUserVoteType(idea: Idea_small | Merged_idea_small): number {
    return idea.vote_details.user_vote_details.vote_type;
  }

  getStatusColor(status: number): string {
  switch (status) {
    case 0: return 'red';
    case 1: return 'green';
    case 2: return 'blue';
    default: return 'gray'; // fallback
  }
}

async open_my_space_idea_modal(card: My_idea ) {
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
    const modalElement = document.getElementById('ticket_details_modal');
    if (modalElement) {
      const modal = bootstrap.Modal.getInstance(modalElement);
      if (modal) modal.hide();
    }
    this.selectedCard = null;
  }

  close_merged_ticket_details_modal() {
    const modalElement = document.getElementById('merged_ticket_details_modal');
    if (modalElement) {
      const modal = bootstrap.Modal.getInstance(modalElement);
      if (modal) modal.hide();
    }
    this.selectedMergedCard = null;
  }

  // open_comments_modal(card: Idea_small | Merged_idea_small) {
  //   this.selectedCommentCard = this.isMergedIdea(card) ? null : card;
  //   const modalElement = document.getElementById('comments_modal');
  //   if (modalElement) new bootstrap.Modal(modalElement).show();
  // }

  // close_comments_modal() {
  //   const modalElement = document.getElementById('comments_modal');
  //   if (modalElement) {
  //     const modal = bootstrap.Modal.getInstance(modalElement);
  //     if (modal) modal.hide();
  //   }
  //   this.selectedCard = null;
  // }

  open_add_idea_modal() {
    const modalElement = document.getElementById('addIdea_modal');
    if (modalElement) new bootstrap.Modal(modalElement).show();
  }

  close_add_idea_modal() {
    const modalElement = document.getElementById('addIdea_modal');
    if (modalElement) {
      const modal = bootstrap.Modal.getInstance(modalElement);
      if (modal) modal.hide();
    }
  }
}