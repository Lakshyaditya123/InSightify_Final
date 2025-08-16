import { Component, OnInit, AfterViewInit, ViewChild, ElementRef} from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { Navbar } from '../../components/navbar/navbar';
import { IdeaDetails } from '../../components/idea-details/idea-details';
import { MergedIdeaDetails } from '../../components/merged-idea-details/merged-idea-details';
import { AuthService } from '../../services/auth';
import { IdeaService } from '../../services/idea';
import { ApiResponse, CurrUser, Idea_large, Merged_idea_large, Idea_small, Merged_idea_small, TagsList, User_idea_details } from '../../services/api-interfaces';

declare var bootstrap: any;

@Component({
  selector: 'app-admin-screen',
  templateUrl: './admin-screen.html',
  styleUrls: ['./admin-screen.css'],
  standalone: true,
  imports: [CommonModule, Navbar, IdeaDetails, MergedIdeaDetails, MatSnackBarModule],
})
export class AdminScreen implements OnInit, AfterViewInit {
  // Arrays for displaying ideas
  all_cards: Idea_small[] = [];
  all_merged_cards: Merged_idea_small[] = [];

  // Master lists to hold original, unfiltered data
  unfiltered_cards: Idea_small[] = [];
  unfiltered_merged_cards: Merged_idea_small[] = [];

  selectedCard: Idea_large | null = null;
  selectedMergedCard: Merged_idea_large | null = null;
  
  currentUserId: number = -1;
  currentUser!: CurrUser;
  model_opened = false;
  showMergedIdea = true;
  isMerging = false;
  isIdeaRemoved = false;
  isClicked=false;
  @ViewChild('modelContent') modelContent!: ElementRef;
  modalWidth: number = 0;
  updatedTagsList: TagsList[] = [];
  userIdeaDetails!:User_idea_details[];
  removeIdeaIds:number[]=[];
  removedCards: User_idea_details[]=[];
  // New properties for the confirmation modal
  showRemoveConfirmModal = false;
  ideaToRemove: User_idea_details | null = null;

  constructor(
    private router: Router,
    private authService: AuthService,
    private ideaService: IdeaService,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit() {
    const currentUser: CurrUser | null = this.authService.getCurrentUser();
    if (currentUser) {
      this.currentUser = currentUser;
      this.currentUserId = currentUser.user_id;
      this.get_all_ideas();
    } else {
      this.router.navigate(['/login']);
      console.error('User not logged in!');
    }
  }

  ngAfterViewInit() {
    const ticket_modal = document.getElementById('ticket_details_modal');
    ticket_modal?.addEventListener('hidden.bs.modal', () => {
      this.close_ticket_details_modal();
    });

    const merged_ticket_modal = document.getElementById('merged_ticket_details_modal');
    merged_ticket_modal?.addEventListener('hidden.bs.modal', () => {
      this.close_merged_ticket_details_modal();
    });
  }

  onSearchReceived(searchTerm: string) {
    const lowerCaseSearchTerm = searchTerm.toLowerCase().trim();

    if (!lowerCaseSearchTerm) {
      this.all_cards = [...this.unfiltered_cards];
      this.all_merged_cards = [...this.unfiltered_merged_cards];
      return;
    }

    this.all_cards = this.unfiltered_cards.filter(card =>
      card.idea_details.title.toLowerCase().includes(lowerCaseSearchTerm) ||
      card.idea_details.subject.toLowerCase().includes(lowerCaseSearchTerm)||
      card.user_details.name.toLowerCase().includes(lowerCaseSearchTerm)
    );

    this.all_merged_cards = this.unfiltered_merged_cards.filter(card =>
      card.merged_idea_details.title.toLowerCase().includes(lowerCaseSearchTerm) ||
      card.merged_idea_details.subject.toLowerCase().includes(lowerCaseSearchTerm)||
      card.user_idea_details.some(user => user.user_details.name.toLowerCase().includes(lowerCaseSearchTerm))
    );
  }

  get_all_ideas() {
    this.ideaService.get_all_admin_main_walls().subscribe((res: ApiResponse) => {
      if (res.errCode === 0 && res.datarec) {
        this.unfiltered_cards = res.datarec.all_ideas || [];
        this.unfiltered_merged_cards = res.datarec.all_merged_ideas || [];
        this.all_cards = [...this.unfiltered_cards];
        this.all_merged_cards = [...this.unfiltered_merged_cards];
      } else {
        console.error("Failed to load admin ideas:", res.message);
      }
    });
  }

    async showChildIdea(card_id:number){
    if(!this.isMerging){
      this.showMergedIdea=false;
      this.isClicked=true;
      const result: ApiResponse = await firstValueFrom(
        this.ideaService.get_idea(card_id, null, this.currentUserId)
      );

      if (result.errCode === 0 && result.datarec) {
        console.log("show children method")
        this.selectedCard = result.datarec;
      } else {
        console.error("Failed to get idea:", result.message);
      }
    }
  }

  removeThisIdea(user: User_idea_details) {
    this.ideaToRemove = user;
    this.showRemoveConfirmModal = true;
  }

  confirmRemoveIdea() {
    if (!this.ideaToRemove) {
      return; 
    }
    this.showMergedIdea = true;
    this.isIdeaRemoved = true;
    this.removeIdeaIds.push(this.ideaToRemove.idea_details.id);
    this.removedCards.push(this.ideaToRemove)
    this.userIdeaDetails = this.userIdeaDetails.filter(
      obj => obj.idea_details.id !== this.ideaToRemove!.idea_details.id
    );
    this.cancelRemoveIdea();
  }
  
  cancelRemoveIdea() {
    this.showRemoveConfirmModal = false;
    this.ideaToRemove = null;
  }

  async RemergeIdeas(){
    this.isMerging=true;
    this.isIdeaRemoved=false;
    const payload={merged_idea_id:this.selectedMergedCard?.merged_idea_details.id,idea_id_list: this.userIdeaDetails.map(item => item.idea_details.id)}
    try{
      const result: ApiResponse= await firstValueFrom(this.ideaService.remerge_these_ideas(payload));
      if (result.errCode === 0 && result.datarec) {
          this.showSuccess('Idea merged successfully!');
          Object.assign(this.selectedMergedCard!.merged_idea_details, {
            title: result.datarec.title,
            subject: result.datarec.subject,
            content: result.datarec.content
          });
          this.isMerging = false
        } else {
          this.showError('Failed to merge Ideas');
          console.error("Failed to get idea:", result.message);
        }
    }catch (error) {
      console.error('Error Merging Ideas:', error);
    }
  }

  async onApprove(idea_id: number|null, merged_idea_id:number|null, merged_idea_details:any|null, removed_idea_ids: number[]|null) {
    const payload={idea_id:idea_id, merged_idea_id:merged_idea_id, status: 1, merged_idea_details: merged_idea_details,removed_idea_ids:removed_idea_ids}
    const result: ApiResponse= await firstValueFrom(this.ideaService.update_user_idea(payload));
    if (result.errCode === 0 && result.datarec) {
        this.showSuccess('Idea Approved');
       for (const card of this.removedCards){
        if (card.idea_details.status===0){
        const removedIdea={
        user_details: {
          id: card.user_details.id,
          name: card.user_details.name,
          profile_picture: card.user_details.profile_picture
        },
        idea_details: {
          id: card.idea_details.id,
          title: card.idea_details.title,
          subject: card.idea_details.subject,
          status: card.idea_details.status,
          created_at: "",
          comments_count: 0
        },
        vote_details: {
          user_vote_details:{
            vote_id: 0,
            vote_type: 0
            },
          vote_details: {
            upvotes: 0,
            downvotes: 0,
            total: 0
            }
        }
    }
    this.all_cards.push(removedIdea)
  }
    if (merged_idea_id!==null) this.all_merged_cards = this.all_merged_cards.filter(card => card.merged_idea_details.id !== this.selectedMergedCard?.merged_idea_details.id);
    else this.all_cards = this.all_cards.filter(card => card.idea_details.id !== this.selectedCard?.idea_details.id);

  }
      } else {
        this.showError('Failed to Approve Idea');
        console.error("Failed to get idea:", result.message);
      }
  }


  async onDecline(idea_id: number|null, merged_idea_id:number|null) {
    const payload={idea_id:idea_id, merged_idea_id:merged_idea_id, status: -1}
    const result: ApiResponse= await firstValueFrom(this.ideaService.update_user_idea(payload));
    if (result.errCode === 0 && result.datarec) {
        this.showSuccess('Idea Declined');
        if (merged_idea_id!==null) this.all_merged_cards = this.all_merged_cards.filter(card => card.merged_idea_details.id !== this.selectedMergedCard?.merged_idea_details.id);
        else this.all_cards = this.all_cards.filter(card => card.idea_details.id !== this.selectedCard?.idea_details.id);
      } else {
        console.error("Failed to get idea:", result.message);
        this.showError('Failed to Decline Idea');
      }
  }

  async open_ticket_details_modal(card: Idea_small,isVisible:boolean=false ) {
    this.model_opened=true;
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
      if (modalElement) {
        new bootstrap.Modal(modalElement).show();
      }
    } catch (error: any) {
      console.error('Error fetching idea details:', error);
    }
  }
  
  async open_merged_ticket_details_modal(card: Merged_idea_small,isVisible:boolean=false ) {
    this.model_opened=false;
    try {
      const result: ApiResponse = await firstValueFrom(
        this.ideaService.get_idea(null, card.merged_idea_details.id, this.currentUserId)
      );
  
      if (result.errCode === 0 && result.datarec) {
        this.selectedMergedCard = result.datarec; 
        this.userIdeaDetails=this.selectedMergedCard!.user_idea_details
      } else {
        console.error("Failed to fetch merged idea details:", result.message);
      }
  
      const modalElement = document.getElementById('merged_ticket_details_modal');
      if (modalElement) {
        new bootstrap.Modal(modalElement).show();
      }
    } catch (error) {
      console.error("Error loading merged idea details:", error);
    }
  }
  close_ticket_details_modal() {
    const mainBtn = document.querySelector('.add-more-btn') as HTMLElement;
    if (mainBtn) mainBtn.focus();
    else document.body.focus();
    const modalElement = document.getElementById('ticket_details_modal');
    if (modalElement) {
      const modal = bootstrap.Modal.getInstance(modalElement);
      if (modal) modal.hide();
    }
    setTimeout(() => {
    this.selectedCard = null;
    window.location.reload();
    }, 150);
  }

  close_merged_ticket_details_modal() {
    const mainBtn = document.querySelector('.add-more-btn') as HTMLElement;
    if (mainBtn) mainBtn.focus();
    else document.body.focus();
    const modalElement = document.getElementById('merged_ticket_details_modal');
    if (modalElement) {
      const modal = bootstrap.Modal.getInstance(modalElement);
      if (modal) modal.hide();
    }
    setTimeout(() => {
    this.selectedMergedCard = null;
    this.showMergedIdea=true;
    this.isIdeaRemoved=false;
    window.location.reload();
     }, 150);

  }

    showSuccess(message: string) {
    this.snackBar.open(message, 'Close', {
      duration: 3000,
      panelClass: ['snack-success'],
    });
  }

  showError(message: string) {
    this.snackBar.open(message, 'Close', {
      duration: 3000,
      panelClass: ['snack-error'],
    });
  }
}
