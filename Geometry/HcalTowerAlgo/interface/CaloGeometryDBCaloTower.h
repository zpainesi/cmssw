#ifndef Geometry_HcalTowerAlgo_CaloGeometryDBCaloTower_h
#define Geometry_HcalTowerAlgo_CaloGeometryDBCaloTower_h

#include "Geometry/CaloEventSetup/interface/CaloGeometryDBEP.h"

namespace calogeometryDBEPimpl {
  template <>
  struct AdditionalTokens<CaloTowerGeometry> {
    void makeTokens(edm::ESConsumesCollectorT<CaloTowerGeometry::AlignedRecord>& cc) {
      topology = cc.consumesFrom<CaloTowerTopology, HcalRecNumberingRecord>(edm::ESInputTag{});
    }
    edm::ESGetToken<CaloTowerTopology, HcalRecNumberingRecord> topology;
  };
}

#endif
