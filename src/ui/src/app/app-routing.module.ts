import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BoxViewComponent } from './Components/box-view/box-view.component';
import { BoxesComponent } from './Components/boxes/boxes.component';

const routes: Routes = [
  {
    path: '',
    redirectTo: 'boxes',
    pathMatch: 'full'
  },
  {
    path: 'boxes',
    component: BoxesComponent
  },
  {
    path: 'box/:id/view',
    component: BoxViewComponent
  },
  {
    path: '**',
    redirectTo: '/boxes'
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
