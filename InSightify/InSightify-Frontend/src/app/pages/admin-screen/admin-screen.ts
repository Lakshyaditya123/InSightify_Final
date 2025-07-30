import { Component, OnInit, AfterViewInit, ViewChild, ElementRef} from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { firstValueFrom } from 'rxjs';

// Import child components and services
import { Navbar } from '../../components/navbar/navbar';
import { IdeaDetails } from '../../components/idea-details/idea-details';
import { MergedIdeaDetails } from '../../components/merged-idea-details/merged-idea-details';
import { AuthService } from '../../services/auth';
import { IdeaService } from '../../services/idea';
import { ApiResponse, CurrUser, Idea_large, Merged_idea_large, Idea_small, Merged_idea_small} from '../../services/api-interfaces';

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
  all_cards: Idea_small[] = [];
  all_merged_cards: Merged_idea_small[] = [];
  selectedCard: Idea_large | null = null;
  selectedMergedCard: Merged_idea_large | null = null;

  
  // State for managing the modal
  currentUserId: number = -1;
  currentUser!:CurrUser;
  model_opened=false;
  showMergedIdea=true;
  @ViewChild('modelContent') modelContent!:ElementRef;
  modalWidth: number = 0;

  constructor(
    private router: Router, 
    private authService: AuthService,
    private ideaService: IdeaService 
  ) {}

  ngOnInit() {
    const currentUser: CurrUser | null = this.authService.getCurrentUser();
    if (currentUser) {
      this.currentUser=currentUser
      this.currentUserId = currentUser.user_id;
      this.get_all_ideas();
    } else {
      this.router.navigate(['/']);
      console.error('User not logged in!');
    }
  }

   ngAfterViewInit() {
    const ticket_modal=document.getElementById('ticket_details_modal');
    ticket_modal?.addEventListener('shown.bs.modal', () => {
      this.modalWidth = this.modelContent.nativeElement.offsetWidth;
    })
    ticket_modal?.addEventListener('hidden.bs.modal',()=>{
      this.close_ticket_details_modal();
    })

    const merged_ticket_modal=document.getElementById('merged_ticket_details_modal');
    merged_ticket_modal?.addEventListener('shown.bs.modal', () => {
      this.modalWidth = this.modelContent.nativeElement.offsetWidth;
    })
    merged_ticket_modal?.addEventListener('hidden.bs.modal',()=>{
      this.close_merged_ticket_details_modal();
    })
  }

  async showChildIdea(card_id:number){
    console.log("Method triggered");
    this.showMergedIdea=false;
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

  get_all_ideas() {
  this.ideaService.get_all_admin_main_walls().subscribe((res: ApiResponse) => {
    if (res.errCode === 0 && res.datarec?.all_ideas) {
      this.all_cards = res.datarec.all_ideas;
      this.all_merged_cards = res.datarec.all_merged_ideas;
      console.log("all_merged_ideas", this.all_merged_cards);
    } else {
      console.error("Failed to load ideas:", res.message);
    }
  });
  }

  onApprove(idea: any) {

  }


  onDecline(idea: any) {

  }

  // onSwitchToUser() {
  //   this.router.navigate(['/homescreen']);
  // }


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
        this.selectedMergedCard = result.datarec; // Full Merged_idea_large
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
     }, 150);
  }
}
