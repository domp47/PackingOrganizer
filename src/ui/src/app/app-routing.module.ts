import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BoxEditComponent } from './Components/box-edit/box-edit.component';
import { BoxViewComponent } from './Components/box-view/box-view.component';
import { BoxesComponent } from './Components/boxes/boxes.component';
import { ItemEditComponent } from './Components/item-edit/item-edit.component';

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
    path: 'box/:id/edit',
    component: BoxEditComponent
  },
  {
    path: 'box/:parentId/item/0/edit',
    component: ItemEditComponent
  },
  {
    path: '**',
    redirectTo: '/boxes'
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { useHash: false })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
