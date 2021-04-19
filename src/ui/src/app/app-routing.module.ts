import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BoxDisplayComponent } from './Components/box-display/box-display.component';

const routes: Routes = [
  {
    path: '',
    redirectTo: 'box',
    pathMatch: 'full'
  },
  {
    path: 'box',
    component: BoxDisplayComponent
  },
  {
    path: '**',
    redirectTo: '/box'
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
