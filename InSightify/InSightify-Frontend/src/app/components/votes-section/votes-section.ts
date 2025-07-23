import { Component, Input } from '@angular/core';
import { Merged_idea_small, Idea_small, ApiResponse, Merged_idea_large } from '../../services/api-interfaces';
import { IdeaService } from '../../services/idea';
import { firstValueFrom } from 'rxjs';
import {CommonModule} from '@angular/common';
@Component({
  selector: 'app-votes-section',
  imports: [CommonModule],
  templateUrl: './votes-section.html',
  styleUrl: './votes-section.css'
})
export class VotesSection {
  @Input() card!: any;
  @Input() currentUserId!: number


  constructor(private ideaService: IdeaService) {}

  isMergedIdea(idea: any): idea is Merged_idea_large | Merged_idea_small {
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
}
