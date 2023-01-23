// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Components/SphereComponent.h"
#include "Components//BoxComponent.h"
#include "Components//SplineComponent.h"
#include "JMBasicScatter.generated.h"

USTRUCT()
struct FGridPoint
{
	GENERATED_BODY()

	UPROPERTY()
	FVector Location;

	UPROPERTY()
	FColor PointColor;
};

UCLASS()
class EDITORTOOLSSANDBOX_API AJMBasicScatter : public AActor
{
	GENERATED_BODY()
	
public:	
	// Sets default values for this actor's properties
	AJMBasicScatter();

	virtual void PostEditChangeProperty(FPropertyChangedEvent& PropertyChangedEvent) override;
	virtual void OnConstruction(const FTransform& Transform) override;
	virtual void PostEditMove(bool bFinished);

private:

	//Variables
	USceneComponent* SceneComp;
	bool bDelegatesEnabled = false;
	TArray<FGridPoint> CreatedPoints;
	FRandomStream Randomize;

	//Functions
	void PostActorMoved(AActor* Actor);
	void PostActorAdded(AActor* Actor);
	void PostActorDeleted(AActor* Actor);

	 TArray<FGridPoint> CreateGridPoints();
	 void DisplayGridPoints();
	
	//UProperties
	UPROPERTY(EditAnywhere, Category = "Main Settings")
	int32 RandomSeed = 0;

	UPROPERTY(EditAnywhere, Category = "Main Settings")
	float InstanceSpacing = 500.f;

	UPROPERTY(EditAnywhere, Category = "Main Settings", meta = (ClampMin = "0", UIMin = "0", ClampMax = "1", UIMax = "1"))
	float OffsetPercentage = 0.5f;	

	UPROPERTY(EditAnywhere, Category = "Instances")
	UStaticMesh* StaticMesh;

	UPROPERTY(EditAnywhere, Category = "Instances")
	AActor* ScatterSurface;

	
	



};
