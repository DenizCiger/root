// @(#):$Id$
// Author: M.Gheata
/*************************************************************************
 * Copyright (C) 1995-2002, Rene Brun and Fons Rademakers.               *
 * All rights reserved.                                                  *
 *                                                                       *
 * For the licensing terms see $ROOTSYS/LICENSE.                         *
 * For the list of contributors see $ROOTSYS/README/CREDITS.             *
 *************************************************************************/

#ifndef ROOT_TGeoPgonEditor
#define ROOT_TGeoPgonEditor

#include "TGWidget.h"
#include "TGeoPconEditor.h"

class TGNumberEntry;
class TGTab;

class TGeoPgonEditor : public TGeoPconEditor {

protected:
   Int_t                fNedgesi;           // Initial number of edges
   TGNumberEntry       *fENedges;           // Number entry for nsections

   void CreateEdges() override;

public:
   TGeoPgonEditor(const TGWindow *p = nullptr,
                   Int_t width = 140, Int_t height = 30,
                   UInt_t options = kChildFrame,
                   Pixel_t back = GetDefaultFrameBackground());
   ~TGeoPgonEditor() override;
   void   SetModel(TObject *obj) override;

   void           DoNedges();
   void   DoApply() override;
   void   DoUndo() override;

   ClassDefOverride(TGeoPgonEditor,0)   // TGeoPgon editor
};
#endif
