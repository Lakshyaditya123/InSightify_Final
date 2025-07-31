// import { Component, ElementRef, HostListener, OnInit, ViewChild } from '@angular/core';
// import { CommonModule } from '@angular/common';
// import { firstValueFrom } from 'rxjs';
// import { Navbar } from '../../components/navbar/navbar';
// import { IdeaDetails } from '../../components/idea-details/idea-details';
// import { MergedIdeaDetails } from '../../components/merged-idea-details/merged-idea-details';
// import { CreateAdd } from '../../components/create-add/create-add';
// import { IdeaService } from '../../services/idea';
// import { ApiResponse, Idea_small, Idea_large, Merged_idea_small, My_idea, Merged_idea_large, CurrUser} from '../../services/api-interfaces';
// import { AuthService } from '../../services/auth';
// import { Router } from '@angular/router';
// import { VotesSection } from '../../components/votes-section/votes-section';


// declare var bootstrap: any;

// @Component({
//   selector: 'app-homescreen',
//   standalone: true,
//   imports: [CommonModule, Navbar, IdeaDetails, CreateAdd, MergedIdeaDetails, VotesSection],
//   templateUrl: './homescreen.html',
//   styleUrl: './homescreen.css'
// })
// export class Homescreen implements OnInit {
//   selectedSmallCard: Idea_small | null = null;
//   selectedMergedSmallCard: Merged_idea_small | null = null;
//   selectedCard: Idea_large | null = null;
//   selectedMergedCard: Merged_idea_large | null = null;
//   selectedCommentCard: Comment | null = null;
//   all_cards: Idea_small[] = [];
//   all_merged_cards: Merged_idea_small[] = [];
//   all_my_cards: My_idea[] = [];
//   currentUserId: number = -1;
//     // Master lists to hold original, unfiltered data
//   private unfiltered_cards: Idea_small[] = [];
//   private unfiltered_merged_cards: Merged_idea_small[] = [];
//   mySpace=false;
//   model_opened=false;
//   showMergedIdea=true;
//   isMergedCommentsVisible = false;
//   isIdeaCommentsVisible=false;
//   @ViewChild('modelContent') modelContent!:ElementRef;
//   modalWidth: number = 0;
//   constructor(private ideaService: IdeaService, private authService: AuthService, private router: Router) {}

//   ngOnInit() {
//     const currentUser: CurrUser | null = this.authService.getCurrentUser();
//     if (currentUser) {
//       this.currentUserId = currentUser.user_id;
//       this.get_all_ideas();
//     } else {
//       this.router.navigate(['/']);
//       console.error('User not logged in!');
//     }
//   }

//   navbar_events(event:string){
//     console.log(event);
//   }

//     const add_idea_ticket_modal=document.getElementById('addIdea_modal');
//     add_idea_ticket_modal?.addEventListener('shown.bs.modal', () => {
//       this.modalWidth = this.modelContent.nativeElement.offsetWidth;
//     })
//     add_idea_ticket_modal?.addEventListener('hidden.bs.modal',()=>{
//       this.close_add_idea_modal();
//     })
//   }

//   ngOnDestroy() {
//     // Clean up any subscriptions or resources if needed
//   console.log("Homescreen component destroyed");
//   const modalElement = document.querySelector('.modal-backdrop');
//   if (modalElement) {
//     modalElement.remove();
//   }
//   document.body.classList.remove('modal-open');
// }

//   get_all_ideas() {
//     this.ideaService.get_all_main_walls(this.currentUserId).subscribe((res: ApiResponse) => {
//       if (res.errCode === 0 && res.datarec?.all_ideas) {
//         this.all_cards = res.datarec.all_ideas;
//         this.all_merged_cards = res.datarec.all_merged_ideas;
//         this.all_my_cards = res.datarec.all_my_ideas;
//         console.log("all_merged_ideas", this.all_merged_cards);
//         console.log("all_my_ideas", this.all_my_cards);
//       } else {
//         console.error("Failed to load ideas:", res.message);
//       }
//     });
//   }
import { Component, ElementRef, HostListener, OnInit, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { firstValueFrom } from 'rxjs';
import { Navbar } from '../../components/navbar/navbar';
import { IdeaDetails } from '../../components/idea-details/idea-details';
import { MergedIdeaDetails } from '../../components/merged-idea-details/merged-idea-details';
import { CreateAdd } from '../../components/create-add/create-add';
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
  // Arrays for displaying ideas on the wall
  all_cards: Idea_small[] = [];
  all_merged_cards: Merged_idea_small[] = [];
  
  // Master lists to hold the original, unfiltered data
  unfiltered_cards: Idea_small[] = [];
  unfiltered_merged_cards: Merged_idea_small[] = [];

  all_my_cards: My_idea[] = [];
  currentUserId: number = -1;
  
  // Other component properties...
  selectedSmallCard: Idea_small | null = null;
  selectedMergedSmallCard: Merged_idea_small | null = null;
  selectedCard: Idea_large | null = null;
  selectedMergedCard: Merged_idea_large | null = null;
  mySpace=false;
  model_opened=false;
  showMergedIdea=true;
  isMergedCommentsVisible = false;
  isIdeaCommentsVisible=false;
  @ViewChild('modelContent') modelContent!:ElementRef;
  modalWidth: number = 0;
  constructor(private ideaService: IdeaService, private authService: AuthService, private router: Router) {}

  ngOnInit() {
    const currentUser: CurrUser | null = this.authService.getCurrentUser();
    if (currentUser) {
      this.currentUserId = currentUser.user_id;
      this.get_all_ideas();
    } else {
      this.router.navigate(['/']);
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
  /**
   * Handles the search term emitted from the navbar.
   */
  onSearchReceived(searchTerm: string) {
    const lowerCaseSearchTerm = searchTerm.toLowerCase().trim();

    if (!lowerCaseSearchTerm) {
      // If search is empty, restore the wall to its original state
      this.all_cards = [...this.unfiltered_cards];
      this.all_merged_cards = [...this.unfiltered_merged_cards];
      return;
    }

    // Filter single ideas based on title, subject, or user name
    this.all_cards = this.unfiltered_cards.filter(card =>
      card.idea_details.title.toLowerCase().includes(lowerCaseSearchTerm) ||
      card.idea_details.subject.toLowerCase().includes(lowerCaseSearchTerm) ||
      card.user_details.name.toLowerCase().includes(lowerCaseSearchTerm)
    );

    // Filter merged ideas based on title, subject, or any of the user names
    this.all_merged_cards = this.unfiltered_merged_cards.filter(card =>
      card.merged_idea_details.title.toLowerCase().includes(lowerCaseSearchTerm) ||
      card.merged_idea_details.subject.toLowerCase().includes(lowerCaseSearchTerm) ||
      card.user_idea_details.some(user => user.user_details.name.toLowerCase().includes(lowerCaseSearchTerm))
    );
  }

  get_all_ideas() {
    this.ideaService.get_all_main_walls(this.currentUserId).subscribe((res: ApiResponse) => {
      if (res.errCode === 0 && res.datarec) {
        // Store the original data in our master lists
        this.unfiltered_cards = res.datarec.all_ideas || [];
        this.unfiltered_merged_cards = res.datarec.all_merged_ideas || [];
        
        // The lists displayed on the wall are initially a copy of the master lists
        this.all_cards = [...this.unfiltered_cards];
        this.all_merged_cards = [...this.unfiltered_merged_cards];
        
        this.all_my_cards = res.datarec.all_my_ideas || [];
      } else {
        console.error("Failed to load ideas:", res.message);
      }
    });
  }

  async showChildIdea(card_id:number){
    console.log("Method triggered");
    this.showMergedIdea=false;
    this.isIdeaCommentsVisible=false;
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

getStatusColor(status: number): string {
  switch (status) {
    case -1: return 'red';
    case 0: return 'gray';
    case 1: return 'green';
    default: return 'gray'; // fallback
  }
}

getCommentsDisplay(count: number): string {
    return count >= 1000 ? (count / 1000).toFixed(1) + 'k' : count.toString();
}

toggleMergedCommentsVisibility() {
    this.isMergedCommentsVisible = !this.isMergedCommentsVisible;
  }

toggleIdeaCommentsVisibility() {
    this.isIdeaCommentsVisible = !this.isIdeaCommentsVisible;
  }

async open_my_space_idea_modal(card: My_idea, isVisible:boolean=false) {
  this.mySpace = true;
  this.model_opened=true;
  this.selectedSmallCard = this.all_cards.find(idea => idea.idea_details.id === card.idea_id) || null;
  this.isIdeaCommentsVisible = isVisible;
  
  try {
    const result: ApiResponse = await firstValueFrom(
      this.ideaService.get_idea(card.idea_id, null, this.currentUserId)
    );

    if (result.errCode === 0 && result.datarec) {
      console.log("open my space idea modal triggered");
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


async open_ticket_details_modal(card: Idea_small,isVisible:boolean=false ) {
  this.selectedSmallCard=card;
  this.isIdeaCommentsVisible = isVisible;
  this.model_opened=true;
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
    if (modalElement) {
      new bootstrap.Modal(modalElement).show();
    }
  } catch (error: any) {
    console.error('Error fetching idea details:', error);
  }
}

async open_merged_ticket_details_modal(card: Merged_idea_small,isVisible:boolean=false ) {
  this.selectedMergedSmallCard = card;
  this.isMergedCommentsVisible = isVisible;
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
    this.isIdeaCommentsVisible = false;
    this.selectedSmallCard = null;
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
    this.isMergedCommentsVisible = false;
    this.showMergedIdea=true;
    this.selectedMergedSmallCard = null;
     }, 150);
  }

  open_add_idea_modal() {
    const modalElement = document.getElementById('addIdea_modal');
    if (modalElement) {
      new bootstrap.Modal(modalElement).show();
    }
  }

  close_add_idea_modal() {
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